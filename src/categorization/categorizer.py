import json
import re
from datetime import datetime as dt
import google.generativeai as genai
import os
import asyncio
from openai import OpenAI, AsyncOpenAI
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import ast
# Safety configuration for Gemini
safe = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

def extract_assistant_response(raw_output, prompt):
        """
        Extract the security vulnerability information and format it as proper JSON
        regardless of how the LLM formats its output.
        """
        # Remove the original prompt if it's included
        if prompt in raw_output:
            response = raw_output.split(prompt, 1)[1]
        else:
            response = raw_output
        
        # Handle chat model markers
        if "<|assistant|>" in response:
            response = response.split("<|assistant|>", 1)[1].strip()
        elif "\n<|assistant|>\n" in response:
            response = response.split("\n<|assistant|>\n", 1)[1].strip()
        
        # Remove trailing tokens
        for end_token in ["</s>", "<|endoftext|>"]:
            if end_token in response:
                response = response.split(end_token, 1)[0].strip()
        
        # Initialize the structure we want to extract
        result = {
            "cwe_category": "Unknown",
            "explanation": "",
            "cause": "",
            "impact": ""
        }
        
        # Find CWE ID
        cwe_match = re.search(r'CWE[- ](\d+)', response)
        if cwe_match:
            result["cwe_category"] = f"CWE-{cwe_match.group(1)}"
        
        # Find Vendor
        vendor_match = re.search(r'(?:Vendor|vendor)[:\s]+([^:\n]+)', response)
        if vendor_match:
            result["vendor"] = vendor_match.group(1).strip()
        
        # Find Cause
        cause_match = re.search(r'(?:Cause|cause)[:\s]+([^\n]+(?:\n[^A-Z][^\n]+)*)', response)
        if cause_match:
            result["cause"] = cause_match.group(1).strip()
        
        # Find Impact
        impact_match = re.search(r'(?:Impact|impact)[:\s]+([^\n]+(?:\n[^A-Z][^\n]+)*)', response)
        if impact_match:
            result["impact"] = impact_match.group(1).strip()
        
        # Extract explanation - if not explicitly found, use the vulnerability description
        explanation_match = re.search(r'(?:Explanation|explanation|Vulnerability Description)[:\s]+([^\n]+(?:\n[^A-Z][^\n]+)*)', response)
        if explanation_match:
            result["explanation"] = explanation_match.group(1).strip()
        elif "explanation" in response.lower():
            # Try to extract text after "explanation:"
            parts = response.lower().split("explanation:", 1)
            if len(parts) > 1:
                explanation_text = parts[1].split("\n", 1)[0].strip()
                result["explanation"] = explanation_text
        
        # If no separate explanation was found, try to use the description from the prompt
        if not result["explanation"]:
            description_match = re.search(r'Description:\s*```\s*(.*?)\s*```', prompt, re.DOTALL)
            if description_match:
                result["explanation"] = description_match.group(1).strip()
        
        # Clean up any values
        for key in result:
            if isinstance(result[key], str):
                # Remove multiple spaces
                result[key] = re.sub(r'\s+', ' ', result[key]).strip()
                # Remove any remaining backticks
                result[key] = result[key].replace('`', '')
        
        return result

def _extract_category_v2(response):
    """Extract structured data from AI response text."""
    try:
        # Check if response is a list of messages
        if isinstance(response, list) and response:
            # Extract content from the last assistant message
            for item in reversed(response):
                if item.get('role') == 'assistant':
                    text_part = item.get('content', '')
                    break
            else:
                return {
                    "cwe_category": "UNKNOWN",
                    "explanation": "No assistant response found",
                    "vendor": "Unknown",
                    "cause": "",
                    "impact": ""
                }
        else:
            text_part = response

        # Remove any non-JSON text after the JSON block
        text_part = text_part.split('\n\nExplanation:')[0].strip()

        # Try to extract JSON with or without backticks
        patterns = [
            r'```json\s*(\{[\s\S]*?\})\s*```',  # JSON with backticks
            r'\{[\s\S]*?\}'  # Raw JSON
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text_part, re.DOTALL)
            for match in matches:
                try:
                    json_str = match.group(1) if '```' in pattern else match.group(0)
                    json_str = json_str.strip()
                    result = json.loads(json_str)
                    
                    if "Categorization: CWE-ID:" in text_part:
                        cwe_id_match = re.search(r'Categorization: CWE-ID:\s*(CWE-\d+)', text_part)
                        vendor_match = re.search(r'Vendor:\s*(.*?)\n', text_part, re.DOTALL)
                        cause_match = re.search(r'Cause:\s*(.*?)\n', text_part, re.DOTALL)
                        # Extrair impact e explanation usando lógica similar

                        if cwe_id_match and vendor_match and cause_match: # e impact_match e explanation_match:
                            return {
                                "cwe_category": cwe_id_match.group(1).strip(),
                                "explanation": explanation_match.group(1).strip(),  # Adaptar para extrair explanation
                                "vendor": vendor_match.group(1).strip(),
                                "cause": cause_match.group(1).strip(),
                                "impact": impact_match.group(1).strip()  # Adaptar para extrair impact
                            }

                    # Return structured result if all required fields are present
                    if all(k in result for k in ["cwe_category", "explanation", "vendor", "cause", "impact"]):
                        return {
                            "cwe_category": result["cwe_category"],
                            "explanation": result["explanation"],
                            "vendor": result["vendor"],
                            "cause": result["cause"],
                            "impact": result["impact"]
                        }
                except json.JSONDecodeError:
                    continue

        # Fallback to regex extraction if JSON extraction fails
        cwe_id_match = re.search(r'CWE ID:\s*(CWE-\d+)', text_part)
        vendor_match = re.search(r'Vendor:\s*([\w\s]+)', text_part)
        cause_match = re.search(r'Cause:\s*(.*)', text_part)
        impact_match = re.search(r'Impact:\s*(.*)', text_part)
        explanation_match = re.search(r'Explanation:\s*(.*)', text_part, re.DOTALL)

        if cwe_id_match and vendor_match and cause_match and impact_match and explanation_match:
            return {
                "cwe_category": cwe_id_match.group(1).strip(),
                "explanation": explanation_match.group(1).strip(),
                "vendor": vendor_match.group(1).strip(),
                "cause": cause_match.group(1).strip(),
                "impact": impact_match.group(1).strip()
            }

        return {
            "cwe_category": "UNKNOWN",
            "explanation": "Could not extract data",
            "vendor": "Unknown",
            "cause": "",
            "impact": ""
        }
    except Exception as e:
        print(f"Error in _extract_category_v2: {e}")
        return {
            "cwe_category": "UNKNOWN",
            "explanation": str(e),
            "vendor": "Unknown",
            "cause": "",
            "impact": ""
        }

def _extract_category(text_part):
    """Extract JSON from AI response text."""
    # Remove any non-JSON text after the JSON block
    text_part = text_part.split('\n\nExplanation:')[0].strip()
    
    # Try to extract JSON with or without backticks
    patterns = [
        r'```json\s*(\{[\s\S]*?\})\s*```',  # JSON with backticks
        r'\{[\s\S]*?\}'                      # Raw JSON
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text_part, re.DOTALL)
        for match in matches:
            try:
                json_str = match.group(1) if '```' in pattern else match.group(0)
                json_str = json_str.strip()
                result = json.loads(json_str)
                
                # Return structured result if all required fields are present
                if all(k in result for k in ["cwe_category", "explanation", "vendor", "cause", "impact"]):
                    return {
                        "cwe_category": result["cwe_category"],
                        "explanation": result["explanation"],
                        "vendor": result["vendor"],
                        "cause": result["cause"],
                        "impact": result["impact"]
                    }
            except json.JSONDecodeError:
                continue
    
    return {
        "cwe_category": "UNKNOWN",
        "explanation": "",
        "vendor": "Unknown",
        "cause": "",
        "impact": ""
    }

class Categorizer:
    def __init__(self):
        pass

    async def categorize_vulnerability_gpt(self, description):
        client = AsyncOpenAI(api_key=os.environ["CHATGPT_API_KEY"])
        prompt = f"""
        You are a security expert.
        Categorize the following vulnerability description into a CWE category, identify the vendor, and extract the cause and impact of the vulnerability.
        Provide the CWE ID (only the CWE ID of the vulnerability), a brief explanation, the vendor name, the cause of the vulnerability, and its impact.

        Description:
        ```
        {description}
        ```
        Rules for returning the vendor:
        - Return only the official/primary vendor name
        - For open source projects, return the organization maintaining it
        - If multiple vendors are mentioned, return the one responsible for the vulnerable component
        - Normalize variations of the same vendor name
        - If no clear vendor is found, return "Unknown"
        - Use official vendor names where possible and keep the same name for vulnerabilities of the same vendor

        Output:
        ```json
        {{"cwe_category": "CWE-ID", "explanation": "Brief Explanation of the CWE", "vendor": "Vendor Name", "cause": "Cause of the Vulnerability", "impact": "Impact of the Vulnerability"}}
        ```
        """
        try:
            completion = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            result = _extract_category(completion.choices[0].message.content)
            return [result]
        except Exception as e:
            print(f"Error calling ChatGPT API: {e}")
            return [{"cwe_category": "UNKNOWN", "explanation": str(e), "vendor": "Unknown", "cause": "", "impact": ""}]

    async def categorize_vulnerability_gemini(self, description):
        genai_api_key = os.environ.get("GEMINI_API_KEY", "")
        if not genai_api_key:
            print("Gemini API key not found in environment.")
            return [{ "cwe_category": "UNKNOWN", "explanation": "Gemini API key missing", "vendor": "Unknown", "cause": "Unknown", "impact": "Unknown"}]
        genai.configure(api_key=genai_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f"""
        You are a security expert.
        Categorize the following vulnerability description into a CWE category, identify the vendor, and extract the cause and impact of the vulnerability.
        Provide the CWE ID (only the CWE ID of the vulnerability), a brief explanation, the vendor name, the cause of the vulnerability, and its impact.

        Description:
        ```
        {description}
        ```
        Rules for returning the vendor:
        - Return only the official/primary vendor name
        - For open source projects, return the organization maintaining it
        - If multiple vendors are mentioned, return the one responsible for the vulnerable component
        - Normalize variations of the same vendor name
        - If no clear vendor is found, return "Unknown"
        - Use official vendor names where possible and keep the same name for vulnerabilities of the same vendor

        Output:
        ```json
        {{"cwe_category": "CWE-ID", "explanation": "Brief Explanation of the CWE", "vendor": "Vendor Name", "cause": "Cause of the Vulnerability", "impact": "Impact of the Vulnerability"}}
        ```
        """
        try:
            response = await model.generate_content_async(prompt, safety_settings=safe)
            if response.candidates:
                result = _extract_category(response.candidates[0].content.parts[0].text)
                return [result]
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
        return [{"cwe_category": "UNKNOWN", "explanation": "API error", "vendor": "Unknown", "cause": "", "impact": ""}]

    async def categorize_vulnerability_llama(self, description):
        client = AsyncOpenAI(api_key=os.environ["LLAMA_API_KEY"], base_url="https://api.llama-api.com")
        prompt = f"""
        You are a security expert.
        Categorize the following vulnerability description into a CWE category, identify the vendor, and extract the cause and impact of the vulnerability.
        Provide the CWE ID (only the CWE ID of the vulnerability), a brief explanation, the vendor name, the cause of the vulnerability, and its impact.

        Description:
        ```
        {description}
        ```
        Rules for returning the vendor:
        - Return only the official/primary vendor name
        - For open source projects, return the organization maintaining it
        - If multiple vendors are mentioned, return the one responsible for the vulnerable component
        - Normalize variations of the same vendor name
        - If no clear vendor is found, return "Unknown"
        - Use official vendor names where possible and keep the same name for vulnerabilities of the same vendor

        Output:
        ```json
        {{"cwe_category": "CWE-ID", "explanation": "Brief Explanation of the CWE", "vendor": "Vendor Name", "cause": "Cause of the Vulnerability", "impact": "Impact of the Vulnerability"}}
        ```
        """
        retries = 3
        for i in range(retries):
            try:
                response = await client.chat.completions.create(
                    model="llama3.1-70b",
                    messages=[{"role": "user", "content": prompt}]
                )
                return [_extract_category(response.choices[0].message.content)]
            except Exception as e:
                print(f"Error calling Llama API (attempt {i+1}/{retries}): {e}")
                await asyncio.sleep(2 ** i)  # Exponential backoff
        return [{"cwe_category": "UNKNOWN", "explanation": str(e), "vendor": "Unknown", "cause": "", "impact": ""}]

    async def categorize_vulnerability_combined(self, description):
        """
        Combines results from all AI providers using weighted voting.
        """
        gemini_result = await self.categorize_vulnerability_gemini(description)
        gpt_result = await self.categorize_vulnerability_gpt(description)
        llama_result = await self.categorize_vulnerability_llama(description)

        # Use voting system to combine results
        return self.combine_results(
            gemini_result,
            gpt_result,
            llama_result
        )

    async def categorize_vulnerability_default(self, description):
        api_key = os.getenv('DEFAULT_API_KEY')
        base_url = os.getenv('DEFAULT_API_URL')
        model = os.getenv('DEFAULT_API_MODEL')
        
        client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        prompt = f"""
        You are a security expert.
        Categorize the following vulnerability description into a CWE category, identify the vendor, and extract the cause and impact of the vulnerability.
        Provide the CWE ID (only the CWE ID of the vulnerability), a brief explanation, the vendor name, the cause of the vulnerability, and its impact.

        Description:
        ```
        {description}
        ```
        Rules for returning the vendor:
        - Return only the official/primary vendor name
        - For open source projects, return the organization maintaining it
        - If multiple vendors are mentioned, return the one responsible for the vulnerable component
        - Normalize variations of the same vendor name
        - If no clear vendor is found, return "Unknown"
        - Use official vendor names where possible and keep the same name for vulnerabilities of the same vendor

        Output:
        ```json
        {{"cwe_category": "CWE-ID", "explanation": "Brief Explanation of the CWE", "vendor": "Vendor Name", "cause": "Cause of the Vulnerability", "impact": "Impact of the Vulnerability"}}
        ```
        """
        try:
            completion = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            result = _extract_category(completion.choices[0].message.content)
            return [result]
        except Exception as e:
            print(f"Error calling ChatGPT API: {e}")
            return [{"cwe_category": "UNKNOWN", "explanation": str(e), "vendor": "Unknown", "cause": "", "impact": ""}]


    async def categorize_vulnerability_provider(self, description):
        api_key = os.getenv('PROVIDER_API_KEY')
        base_url = os.getenv('PROVIDER_API_URL')
        model = os.getenv('PROVIDER_API_MODEL')
        type = os.getenv("PROVIDER_TYPE")
        config = os.getenv("PROVIDER_CONFIG")
                  
        prompt = f"""
            You are a security expert.
            Categorize the following vulnerability description into a CWE category, identify the vendor, and extract the cause and impact of the vulnerability.
            Provide the CWE ID (only the CWE ID of the vulnerability), a brief explanation, the vendor name, the cause of the vulnerability, and its impact.

            Description:
            ```
            {description}
            ```
            Rules for returning the vendor:
            - Return only the official/primary vendor name
            - For open source projects, return the organization maintaining it
            - If multiple vendors are mentioned, return the one responsible for the vulnerable component
            - Normalize variations of the same vendor name
            - If no clear vendor is found, return "Unknown"
            - Use official vendor names where possible and keep the same name for vulnerabilities of the same vendor

            Returns only the result nothing more!
            Example:
                    {{"cwe_category": "CWE-ID", "explanation": "Brief Explanation of the CWE", "vendor": "Vendor Name", "cause": "Cause of the Vulnerability", "impact": "Impact of the Vulnerability"}}

            Output:
            ```json
                {{"cwe_category": "CWE-ID", "explanation": "Brief Explanation of the CWE", "vendor": "Vendor Name", "cause": "Cause of the Vulnerability", "impact": "Impact of the Vulnerability"}}
            ```
            """
            
        if(type == 'api'):
            client = AsyncOpenAI(api_key=api_key, base_url=base_url)
            try:
                completion = await client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
                result = _extract_category(completion.choices[0].message.content)
                return [result]
            except Exception as e:
                print(f"Error calling API: {e}")
                return [{"cwe_category": "UNKNOWN", "explanation": str(e), "vendor": "Unknown", "cause": "", "impact": ""}]
        
        if(type == 'local'):

            local_prompt = f"""
                You are a security expert.
                Categorize the following vulnerability description into a CWE category, identify the vendor, and extract the cause and impact of the vulnerability.
                Provide the CWE ID (only the CWE ID of the vulnerability), a brief explanation, the vendor name, the cause of the vulnerability, and its impact.

                Description:
                ```
                {description}
                ```
                Rules for returning the vendor:
                - Return only the official/primary vendor name
                - For open source projects, return the organization maintaining it
                - If multiple vendors are mentioned, return the one responsible for the vulnerable component
                - Normalize variations of the same vendor name
                - If no clear vendor is found, return "Unknown"
                - Use official vendor names where possible and keep the same name for vulnerabilities of the same vendor

                Format your response as follows:
                CWE ID: <CWE-ID number only>
                Explanation: <brief explanation of the vulnerability>
                Vendor: <vendor name>
                Cause: <cause of the vulnerability>
                Impact: <impact of the vulnerability>
                """

            try:
                tokenizer = AutoTokenizer.from_pretrained(model)
                
                if(config):
                    pairs = config.split(',')

                    # Converter cada par chave=valor em um dicionário
                    config_dict = {}
                    for pair in pairs:
                        key, value = pair.split('=')
                        config_dict[key] = value
                    model = AutoModelForCausalLM.from_pretrained(model,**config_dict)
                else:
                    model = AutoModelForCausalLM.from_pretrained(model)
                
                messages=[{"role": "user", "content": local_prompt}]
                formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False)

                pipe = pipeline("text-generation", model= model, tokenizer = tokenizer, max_new_tokens=250)
                #print(pipe(formatted_prompt)[0]["generated_text"])
                raw_output = pipe(formatted_prompt)[0]["generated_text"]
                result = extract_assistant_response(raw_output, local_prompt)
                #print(result)

                return [result]
            except Exception as e:
                print(f"Error calling local: {e}")
                return [{"cwe_category": "UNKNOWN", "explanation": str(e), "vendor": "Unknown", "cause": "", "impact": ""}]
            
            except Exception as e:
                print(f"Error calling local: {e}")
                return [{"cwe_category": "UNKNOWN", "explanation": str(e), "vendor": "Unknown", "cause": "", "impact": ""}]

    
    def vote(self, responses, field):
        """
        Implement weighted voting for a specific field across AI responses.
        """
        if not responses:
            return "Unknown"

        self.weights = {
            'gemini': 1.0,
            'chatgpt': 1.0,
            'llama': 1.0
        }

        # Count occurrences with weights
        weighted_votes = {}
        for source, response in responses.items():
            value = str(response.get(field, '')).strip()
            if value:
                weight = self.weights.get(source, 1.0)
                weighted_votes[value] = weighted_votes.get(value, 0) + weight

        # Return the value with highest weighted votes
        if weighted_votes:
            return max(weighted_votes.items(), key=lambda x: x[1])[0]
        return "Unknown"

    def combine_results(self, gemini_result, gpt_result, llama_result):
        """
        Combine results from different AI sources using weighted voting.
        """
        responses = {
            'gemini': gemini_result[0] if gemini_result else {},
            'chatgpt': gpt_result[0] if gpt_result else {},
            'llama': llama_result[0] if llama_result else {}
        }

        return [{
            "cwe_category": self.vote(responses, "cwe_category"),
            "explanation": self.vote(responses, "explanation"),
            "vendor": self.vote(responses, "vendor"),
            "cause": self.vote(responses, "cause"),
            "impact": self.vote(responses, "impact")
        }]
    
