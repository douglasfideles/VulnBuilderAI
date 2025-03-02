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
            
            prompt_local = f"""
            You are a security expert.
            Categorize the following vulnerability description into a CWE category, identify the vendor, and extract the cause and impact of the vulnerability.

            Description:
            {description}

            Provide the output in the following format:
            CWE ID: CWE-ID
            Vendor: Vendor Name
            Cause: Cause of the Vulnerability
            Impact: Impact of the Vulnerability
            Explanation: Brief Explanation of the CWE

            Give only the results nothing more.
            """
            messages=[{"role": "user", "content": f"""
                    You are a security expert.
                    Categorize the following vulnerability description:
                    {description}
                    Provide the output in JSON format:
                    {{"cwe_category": "CWE-ID", "explanation": "Brief Explanation", "vendor": "Vendor Name", "cause": "Cause", "impact": "Impact"}}
                """}]


            try:
                tokenizer = AutoTokenizer.from_pretrained(model)
                
                if(config):
                    config_string = config
                    # Dividir a string em chave e valor
                    key, value = config_string.split('=')
                    # Criar um dicionário com a chave e o valor
                    config_dict = {key: value}
                    model = AutoModelForCausalLM.from_pretrained(model, **config_dict)
                else:
                    model = AutoModelForCausalLM.from_pretrained(model)
                
                pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=200)
                response = pipe(messages, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)[0]["generated_text"]

                print(f"RESULTO OF IA RESPONSE: {response}")

                result = _extract_category_v2(response)
                print(f"RESULTO OF CATEGORIZING: {result}")
                return [result]
            
            except Exception as e:
                print(f"Error calling local: {e}")
                return [{"cwe_category": "UNKNOWN", "explanation": str(e), "vendor": "Unknown", "cause": "", "impact": ""}]

