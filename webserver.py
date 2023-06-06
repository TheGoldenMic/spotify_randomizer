import ssl
import threading
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

SERVER_PORT = 6969

ARGS = {}

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("<html><head><title>Bravo</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<script>document.location=\"https://www.youtube.com/watch?v=aHuZ99bcaCg&t=0\"</script>", "utf-8"))
        self.wfile.write(bytes("Bravo", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        query = urlparse(self.path).query
        # print(query)
        try:
            query_components = dict(qc.split("=") for qc in query.split("&"))
            global ARGS
            ARGS = query_components
        except ValueError:
            pass

def create_server(webServer: HTTPServer):
    # print("Server started.")
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain("cert.pem")
    webServer.socket = ctx.wrap_socket(webServer.socket, server_side=True)
    try:
        webServer.serve_forever()
    except:
        pass