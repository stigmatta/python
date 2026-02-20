from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import urllib.parse 

def url_decode(input_str: str | None) -> str | None:
    return None if input_str is None else urllib.parse.unquote_plus(input_str)

class AccessManagerRequestHandler(BaseHTTPRequestHandler):
    def handle_one_request(self):
        '''
            Базова реалізація BaseHTTPRequestHandler не дозволяє впровадити 
            диспетчер доступу, який, у свою чергу, є вимогою нормативних документів,
            зокрема https://tzi.com.ua/downloads/1.1-002-99.pdf 
        '''
        # https://tedboy.github.io/python_stdlib/_modules/BaseHTTPServer.html#BaseHTTPRequestHandler.handle
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            if not self.raw_requestline:
                self.close_connection = 1
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return
            
            # Заміна - усі запити переводяться на єдиний метод access_manager
            mname = 'access_manager'
            if not hasattr(self, mname):
                self.send_error(501, "Method 'access_manager' not overriden")
                return
            method = getattr(self, mname)
            method()

            self.wfile.flush() # actually send the response if not already done.
        except socket.timeout as e:
            # a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return

    def access_manager(self) -> bool:
        mname = 'do_' + self.command
        if not hasattr(self, mname):
            self.send_error(405, "Unsupported method (%r)" % self.command)
            return
        method = getattr(self, mname)
        method()

class RequestHandler(AccessManagerRequestHandler):

    def __init__(self, request, client_address, server):
        self.query_params = {}
        self.api = {
            "method": None,
            "service": None,
            "section": None
        }
        super().__init__(request, client_address, server)

    
    def access_manager(self):
        parts = self.path.split("?", 1)
        self.api["method"] = self.command

        splitted_path = [url_decode(p) for p in parts[0].strip("/").split("/", 1)]

        self.api["service"] = splitted_path[0] if len(splitted_path) > 0 and len(splitted_path[0]) else "home"
        self.api["section"] = splitted_path[1] if len(splitted_path) > 1 and len(splitted_path[1]) else None

        query_string = parts[1] if len(parts) > 1 else None

        if query_string:
            for item in query_string.split("&"):
                if not item:
                    continue
                
                key, value = map(url_decode, item.split("=", 1) if "=" in item else [item, None])
                
                self.query_params[key] = value if key not in self.query_params else [
                    *(self.query_params[key] if isinstance(self.query_params[key], (list, tuple)) else [self.query_params[key]]),
                    value
                ]
        
        return super().access_manager()

    def do_GET(self):

        self.send_response(200, "OK")
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        query_params_links_html = f"""
        <h2>Перевірка query params (Д.З.):</h2>
        <ul>
            <li><a href="/user/auth">Без параметрів (/user/auth)</a></li>
            <li><a href="/user/auth?">Без параметрів з "?" (/user/auth?)</a></li>
            <li><a href="/user/auth?hash=1a2d==&p=50/50&q=who?&x=10&y=20&x=30&json">З повторами ключів та "=" в значенні</a></li>
            <li><a href="/user/auth?hash=1a2d==&p=50/50&q=who?&&x=10&y=20&x=30&json&url=%D0%A3%D0%BD%D1%96%D1%84%D1%96%D0%BA%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B9&%D0%BB%D0%BE%D0%BA%D0%B0%D1%82%D0%BE%D1%80=%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81%D1%96%D0%B2&2+2=4">URL-кодовані параметри та "+"</a></li>
        </ul>
        <hr>
        """

        routes_links_html = f"""
        <h2>Перевірка роутінгу (Д.З.):</h2>
        <ul>
            <li><a href="/">Без параметрів (/)</a></li>
            <li><a href="/user/">(/user/)</a></li>
            <li><a href="/user">(/user)</a></li>
            <li><a href="/user/auth">(/user/auth)</a></li>
            <li><a href="/user/auth/secret">(/user/auth/secret)</a></li>
            <li><a href="/user/%D0%A3%D0%BD%D1%96%D1%84%D1%96%D0%BA%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B9&%D0%BB%D0%BE%D0%BA%D0%B0%D1%82%D0%BE%D1%80=%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81%D1%96%D0%B2&2+2=4">(/user/auth/ENCODED)</a></li>
        </ul>
        <hr>
        """

        self.wfile.write(f"""
            <html>
                <body>
                    {query_params_links_html}
                    <br>
                    <br>
                    {routes_links_html}
                    <b>self.path:</b> {self.path}<br>
                    <b>Параметри (словник):</b> {self.query_params}
                    <b>API:</b> {self.api}
                    <hr>
                    <button onclick="linkClick()">LINK</button>
                    <p id=out></p>
                    <script>
                        function linkClick() {{
                            fetch('/', {{ method: 'LINK' }}).then(response => response.text())
                            .then(data => {{
                                out.innerText = data;
                            }})
                        }}
                    </script>
                </body>
            </html>
        """.encode())

    def do_LINK(self):
        self.send_response(200, "OK")
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("Link method response".encode())

def main() :
    host = '127.0.0.1'
    port = 8080
    endpoint = (host, port)
    http_server = HTTPServer(endpoint, RequestHandler)
    try :
        print(f"Try start server http://{host}:{port}")
        http_server.serve_forever()
    except :
        print("Server stopped")
 
 
if __name__ == '__main__' :
    main()    
    