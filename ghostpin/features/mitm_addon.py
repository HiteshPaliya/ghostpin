"""
GhostPin v5 - Mitmproxy Addon for API Discovery
Ran natively via `mitmdump -s mitm_addon.py`.
Parses live traffic, WebSockets, and GraphQL, feeding it directly into the API Map.
"""
from mitmproxy import http
from mitmproxy import websocket
import urllib.request
import json
import logging

class APIAutoDiscover:
    def __init__(self):
        # The GhostPin server port where we send extracted flows
        self.api_port = 7331  # Default, can be overridden if needed
        import os
        if 'GHOSTPIN_PORT' in os.environ:
            self.api_port = int(os.environ['GHOSTPIN_PORT'])
            
    def _send_to_mapper(self, url: str, method: str, content: str, is_ws: bool = False):
        try:
            flow_data = {
                'request': {
                    'url': url,
                    'method': method,
                    'content_snippet': content[:1024]
                },
                'is_websocket': is_ws
            }
            req = urllib.request.Request(
                f"http://127.0.0.1:{self.api_port}/api/discovery/extract/flow",
                data=json.dumps(flow_data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            urllib.request.urlopen(req, timeout=1)
        except Exception as e:
            logging.debug(f"GhostPin Addon Error: {e}")

    def request(self, flow: http.HTTPFlow):
        """Standard HTTP/HTTPS Request Intercept (plus GraphQL parsing)"""
        url = flow.request.url
        method = flow.request.method
        content = ""
        
        # Parse GraphQL from body
        if flow.request.content:
            try:
                content = flow.request.content.decode('utf-8', errors='ignore')
            except: pass
            
        self._send_to_mapper(url, method, content)

    def websocket_message(self, flow: websocket.WebSocketFlow):
        """WebSocket Frame Intercept"""
        # The URL is the websocket handshake URL
        url = flow.handshake_flow.request.url.replace('http', 'ws')
        msg = flow.messages[-1]
        content = ""
        if isinstance(msg.content, bytes):
            content = msg.content.decode('utf-8', errors='ignore')
        elif isinstance(msg.content, str):
            content = msg.content
            
        direction = "CLIENT_TO_SERVER" if msg.from_client else "SERVER_TO_CLIENT"
        self._send_to_mapper(url, f"WEBSOCKET ({direction})", content, is_ws=True)

addons = [
    APIAutoDiscover()
]
