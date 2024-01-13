import http.server
import http.client
import base64
import json
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer

with open('config.json') as f:
    config = json.loads(f.read())
host = config["listening_address"]
port = config["listening_port"]


class ReverseProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        self.handle_request("POST")

    def do_PUT(self):
        self.handle_request("PUT")

    def do_DELETE(self):
        self.handle_request("DELETE")

    def do_HEAD(self):
        self.handle_request("HEAD")

    def do_OPTIONS(self):
        self.handle_request("OPTIONS")

    def do_PATCH(self):
        self.handle_request("PATCH")

    def do_TRACE(self):
        self.handle_request("TRACE")

    def do_METHOD(self):
        method = self.command
        self.handle_request(method)

    def handle_request(self, method):
        if not self.authenticate():
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Reverse Proxy"')
            self.end_headers()
            self.wfile.write(b'Authentication required')
            self.log_message("Authentication failed for %s", self.client_address)
            return

        target_connection = http.client.HTTPConnection(config["backend_host"], config["backend_port"])
        target_path = self.path

        headers = {header: value for header, value in self.headers.items()}
        user_agent = headers.get('User-Agent', '')
        self.log_message("Forwarding %s request to %s with User-Agent: %s", method, target_path, user_agent)

        target_connection.request(method, target_path, self.get_request_body(), headers=headers)
        target_response = target_connection.getresponse()

        self.send_response(target_response.status)
        [self.send_header(header, value) for header, value in target_response.getheaders()]
        self.end_headers()

        self.wfile.write(target_response.read())
        target_connection.close()

        self.log_message("Request proxied to %s with status %d", target_path, target_response.status)

    def authenticate(self):
        auth_header = self.headers.get('Authorization')
        if auth_header and auth_header.startswith('Basic '):
            credentials = auth_header[len('Basic '):].encode('utf-8')
            decoded_credentials = base64.b64decode(credentials).decode('utf-8')
            username, password = decoded_credentials.split(':', 1)
            if username == config["username"] and password == config["password"]:
                self.log_message("Authentication successful for user: %s", username)
                return True
            else:
                self.log_message("Incorrect credentials provided for user: %s", username)
        return False

    def get_request_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(content_length)


def run():
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, ReverseProxyHandler)
    print(f"Reverse proxy listening at {host} with the port {port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down.")
        httpd.server_close()


if __name__ == '__main__':
    run()
