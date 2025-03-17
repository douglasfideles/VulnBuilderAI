import requests
import json
import os
from .data_source import DataSourceBase

class VulnersExtractor(DataSourceBase):
    async def collect_data(self, search_params):
        vulnerabilities = []
        for param in search_params:
            print(f"Collecting VULNERS data for search parameter: {param}")
            vulners_response = await self.get_vulners_data(param)
            if vulners_response and 'data' in vulners_response and 'search' in vulners_response['data']:
                vulners_vulns = vulners_response['data']['search']
                for vuln in vulners_vulns:
                    vuln['vendor'] = param
                    vulnerabilities.append(vuln)
                print(f"Found {len(vulners_vulns)} Vulners vulnerabilities for {param}")
        return vulnerabilities

    async def get_vulners_data(self, query, skip=0):
        base_url = "https://vulners.com/api/v3/search/search"
        api_key = os.getenv("VULNERS_API_KEY")
        data = {
            'query': query,
            'skip': skip,
            'apiKey': api_key
        }
        try:
            response = requests.post(base_url, data=json.dumps(data))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        return {}

    def normalize_data(self, vulnerability):
        source = vulnerability.get('_source', {})
        return {
            'id': source.get('id'),
            'description': source.get('description'),
            'published': source.get('published'),
            'cvss_score': source.get('cvss', {}).get('score'),
            'severity': source.get('cvss', {}).get('severity'),
            'source': 'vulners'
        }