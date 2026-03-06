"""
GhostPin Enterprise v5 - Automatic API Endpoint Discovery
Combines static AST string extraction from the APK (via vuln_scanner) and dynamic traffic observation (via mitmproxy/Frida)
to automatically build a complete map of the application's backend infrastructure.
"""
import re
from typing import Set, Dict, List
import urllib.parse

class APIEndpointMapper:
    def __init__(self):
        self.discovered_hosts: Set[str] = set()
        self.discovered_endpoints: Dict[str, Dict] = {}
        
        # Regex patterns for finding URLs and IP addresses in static strings
        self.url_pattern = re.compile(r'https?://[a-zA-Z0-9.\-_~]+(?:/[a-zA-Z0-9./\-_~%]+)?(?:\?[a-zA-Z0-9.\-_~=%&]+)?')
        self.ipv4_pattern = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
        self.graphql_pattern = re.compile(r'(mutation|query)\s+[A-Za-z0-9_]+\s*[\({]')

    def extract_from_static_strings(self, strings: List[str]):
        """Runs over the raw strings extracted from dex/so/xml files to find hardcoded endpoints."""
        for s in strings:
            if not isinstance(s, str): continue
            
            # URLs
            for url in self.url_pattern.findall(s):
                self._add_endpoint(url, source='STATIC_APK')
                
            # IP Addresses (often used for staging/C2)
            for ip in self.ipv4_pattern.findall(s):
                # Filter obvious false positives like version numbers
                if ip not in ['0.0.0.0', '127.0.0.1', '255.255.255.255'] and not ip.startswith('1.0.0.'):
                    self._add_endpoint(f"http://{ip}", source='STATIC_APK_IP')

            # GraphQL Queries (if a string looks like a discrete GQL string)
            if self.graphql_pattern.search(s):
                # Add a dummy endpoint to denote a GQL operation was found
                op_name_match = re.search(r'(?:mutation|query)\s+([A-Za-z0-9_]+)', s)
                op_name = op_name_match.group(1) if op_name_match else "UnknownOp"
                self._add_endpoint(f"graphql://operation/{op_name}", source='STATIC_GRAPHQL', method="POST")

    def extract_from_dynamic_flow(self, flow: Dict):
        """Processes a single mitmproxy flow dictionary to add confirmed live endpoints to the map."""
        url = flow.get('request', {}).get('url', '')
        method = flow.get('request', {}).get('method', 'GET')
        req_content = flow.get('request', {}).get('content_snippet', '')
        
        if not url: return
        
        # Detect if this is GraphQL
        if 'graphql' in url.lower() or 'query' in req_content or 'mutation' in req_content:
            try:
                # Basic attempt to pull operation name from payload if JSON
                if '{' in req_content and 'operationName' in req_content:
                    import json
                    parsed = json.loads(req_content)
                    op = parsed.get('operationName', 'Unknown')
                    url = f"{url}?op={op}"
                else:
                     # GQL fallback
                     if "mutation" in req_content: url += " [GraphQL Mutation]"
                     if "query" in req_content: url += " [GraphQL Query]"
            except: pass

        self._add_endpoint(url, source='DYNAMIC_TRAFFIC', method=method)

    def _add_endpoint(self, url: str, source: str, method: str = 'GET'):
        try:
            parsed = urllib.parse.urlparse(url)
            host = parsed.netloc
            if not host: 
                # For weird URIs
                host = parsed.path.split('/')[0] if parsed.path else "unknown"
            
            self.discovered_hosts.add(host)
            
            # Use path as key to deduplicate identical endpoints with different query exact params
            key = f"{method} {host}{parsed.path}"
            if key not in self.discovered_endpoints:
                self.discovered_endpoints[key] = {
                    'url': url,
                    'host': host,
                    'path': parsed.path,
                    'method': method,
                    'sources': set([source]),
                    'params': []
                }
            else:
                 self.discovered_endpoints[key]['sources'].add(source)
                 
            # Aggregate observed params
            if parsed.query:
                params = urllib.parse.parse_qs(parsed.query)
                for p in params.keys():
                    if p not in self.discovered_endpoints[key]['params']:
                        self.discovered_endpoints[key]['params'].append(p)
        except Exception as e:
            pass # Ignore malformed URLs

    def get_map(self) -> Dict:
        """Returns the complete API map as a JSON-serializable dictionary."""
        # Convert sets to lists for JSON
        results = []
        for k, v in self.discovered_endpoints.items():
            ep = dict(v)
            ep['sources'] = list(ep['sources'])
            results.append(ep)
            
        return {
            'hosts': list(self.discovered_hosts),
            'endpoints': sorted(results, key=lambda x: x['host'] + x['path'])
        }

# Global mapper instance
mapper = APIEndpointMapper()
