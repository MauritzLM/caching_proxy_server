
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import cached_property
from urllib.parse import parse_qsl, urlparse
import json

cache = {}
origin = ''

class WebRequestHandler(BaseHTTPRequestHandler):
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))
    
    def get_response(self):
        if self.url.path in cache:
            return json.dumps (
                {
                    "response": cache[self.url.path]
                }
            )
        
        # make request to url/ + path
        # cache response
        
        cache[self.url.path] = 'from cache'

        return json.dumps(
            {
                "response": 'from origin'
            }
        )

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(self.get_response().encode("utf-8"))
        

if __name__ == "__main__":
    error_msg = 'Enter --port <number> --origin <url>'
    
    if(len(sys.argv) != 5):
        sys.exit(error_msg)

    if(sys.argv[1] != '--port'):
        sys.exit(error_msg)

    if(sys.argv[3] != '--origin'):
        sys.exit(error_msg)
    
    port = int(sys.argv[2])
    origin = sys.argv[4]
    headers = {"accept": "application/json"}

    server = HTTPServer(('localhost', port), WebRequestHandler)
    print(f'Starting server on port {port}')
    server.serve_forever()
    