"""Local read-only manifest viewer. Serve only the UI and a configured manifest."""
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path

def serve(manifest,port):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path=='/':
                body=(Path(__file__).parent/'index.html').read_bytes();kind='text/html; charset=utf-8'
            elif self.path=='/manifest.json':
                try:body=json.dumps(json.loads(manifest.read_text())).encode()
                except (OSError,ValueError):self.send_error(503,'Manifest not available');return
                kind='application/json'
            else:self.send_error(404);return
            self.send_response(200);self.send_header('Content-Type',kind)
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    HTTPServer(('127.0.0.1',port),Handler).serve_forever()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,required=True);parser.add_argument('--port',type=int,default=4790)
    args=parser.parse_args();serve(args.manifest,args.port)
