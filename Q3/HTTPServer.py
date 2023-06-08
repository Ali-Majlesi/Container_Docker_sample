from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Global variable to store the current status
current_status = "OK"

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global current_status
        if self.path == '/api/v1/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": current_status}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        global current_status
        if self.path == '/api/v1/status':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_body = json.loads(post_data)
            current_status = request_body.get('status', 'not OK')
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(post_data)
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting server on port 8000...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

