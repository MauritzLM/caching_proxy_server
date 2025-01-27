
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import cached_property
from urllib.parse import parse_qsl, urlparse
import json
import requests

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
        try: 
            if self.url.path in cache:
                print("[Cache]: HIT")
                return json.dumps (
                    {
                        "response": cache[self.url.path]
                    }
                )

            print("[Cache]: MISS")        
            # make request to url + path
            # cache response
            headers = {'content-type': 'application/json; charset=utf8'}
            response = requests.get(f'{origin}{self.url.path}', headers=headers)
            print(response.headers['Content-Type'])
            
            # if response content is json
            if 'application/json' in response.headers['content-type']:
                cache[self.url.path] = response.json()
                return json.dumps(
                {
                    "response": response.json()
                }
            )

            cache[self.url.path] = 'NON JSON response'

            return json.dumps(
                {
                    "response": 'NON JSON response'
                }
            )
        except:
            print("An error occured")

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(self.get_response().encode("utf-8"))
        

if __name__ == "__main__":
    error_msg = 'Enter --port <number> --origin <url>'
    
    if len(sys.argv) != 5:
        sys.exit(error_msg)

    if sys.argv[1] != '--port':
        sys.exit(error_msg)

    if sys.argv[3] != '--origin':
        sys.exit(error_msg)
    
    port = int(sys.argv[2])

    origin = sys.argv[4].rstrip('/')
   
    server = HTTPServer(('localhost', port), WebRequestHandler)
    print(f'Starting server on port {port}')
    server.serve_forever()
    