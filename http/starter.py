from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse 

def url_decode(input_str: str | None) -> str | None:
    return None if input_str is None else urllib.parse.unquote_plus(input_str)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parts = self.path.split("?", 1)
        full_path = parts[0]
        query_string = parts[1] if len(parts) > 1 else None
        
        query_params = {}
        
        if query_string:
            for item in query_string.split("&"):
                if not item:
                    continue
                
                key, value = map(url_decode, item.split("=", 1) if "=" in item else [item, None])
                
                query_params[key] = value if key not in query_params else [
                    *(query_params[key] if isinstance(query_params[key], (list, tuple)) else [query_params[key]]),
                    value
                ]

        self.send_response(200, "OK")
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        links_html = f"""
        <h2>Тестові посилання (Д.З.):</h2>
        <ul>
            <li><a href="/user/auth">Без параметрів (/user/auth)</a></li>
            <li><a href="/user/auth?">Без параметрів з "?" (/user/auth?)</a></li>
            <li><a href="/user/auth?hash=1a2d==&p=50/50&q=who?&x=10&y=20&x=30&json">З повторами ключів та "=" в значенні</a></li>
            <li><a href="/user/auth?hash=1a2d==&p=50/50&q=who?&&x=10&y=20&x=30&json&url=%D0%A3%D0%BD%D1%96%D1%84%D1%96%D0%BA%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B9&%D0%BB%D0%BE%D0%BA%D0%B0%D1%82%D0%BE%D1%80=%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81%D1%96%D0%B2&2+2=4">URL-кодовані параметри та "+"</a></li>
        </ul>
        <hr>
        """

        self.wfile.write(f"""
            <html>
                <body>
                    <h1>Аналізатор запитів</h1>
                    {links_html}
                    <b>self.path:</b> {self.path}<br>
                    <b>Шлях:</b> {full_path}<br>
                    <b>Query String:</b> {query_string}<br>
                    <b>Параметри (словник):</b> {query_params}
                </body>
            </html>
        """.encode())

def main():
    host = '127.0.0.1'
    port = 8080
    endpoint = (host, port)
    http_server = HTTPServer(endpoint, RequestHandler)
    try:
        print(f"Сервер запущено: http://{host}:{port}")
        http_server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер зупинено")

if __name__ == '__main__':
    main()