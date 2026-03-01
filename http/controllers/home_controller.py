from http.server import BaseHTTPRequestHandler


class HomeController:
    def __init__(self, handler: BaseHTTPRequestHandler):
        self.handler = handler

    def do_GET(self):
        self.handler.send_response(200, "OK")
        self.handler.send_header("Content-type", "text/html; charset=utf-8")
        self.handler.end_headers()
        
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

        self.handler.wfile.write(f"""
            <html>
                <body>
                    <h1>HTTP</h1>
                    <img src="/Python.png" alt="Python logo" width="200">
                    {query_params_links_html}
                    <br>
                    <br>
                    {routes_links_html}
                    <b>self.path:</b> {self.handler.path}<br>
                    <b>Параметри (словник):</b> {self.handler.query_params}
                    <b>API:</b> {self.handler.api}
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
        self.handler.send_response(200, "OK")
        self.handler.send_header("Content-type", "text/plain; charset=utf-8")
        self.handler.end_headers()
        self.handler.wfile.write("Link method response".encode())