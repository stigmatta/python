
from controllers.controller_rest import ControllerRest


class HomeController(ControllerRest):

    def do_GET(self):
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

        self.html = f"""
            <html>
                <body>
                    <h1>HTTP</h1>
                    <img src="/static/Python.png" alt="Python logo" width="200">   
                    {query_params_links_html}
                    <br>
                    <br>
                    {routes_links_html}
                    <b>self.path:</b> {self.handler.path}<br>
                    <b>Параметри (словник):</b> {self.handler.query_params}
                    <b>API:</b> {self.handler.api}
                    <hr>
                    <button onclick="onClick('LINK')">LINK</button>
                    <button onclick="onClick('POST')">POST</button>
                    <button onclick="onClick('GET', 'user')">GET user</button>
                    <button onclick="onClick('POST', 'user')">POST user</button>

                    <button onclick="onClick('GET', 'no')">GET no module</button>
                    <button onclick="onClick('GET', 'noclass')">GET no controller</button>
                    <button onclick="onClick('GET', 'noinit')">GET no constructor</button>
                    <button onclick="onClick('GET', 'noserve')">GET no serve method</button>
                    <button onclick="onClick('GET', 'exserve')">GET exception in serve</button>
                    <p id=out></p>
                    <script>
                        function onClick(method, service='') {{
                            fetch(`/${{service}}`, {{
                                method: method 
                            }}).then(response => response.text())
                            .then(data => {{
                                out.innerText = data;
                            }})
                        }}
                    </script>
                </body>
            </html>
        """
        self.content_type = "text/html; charset=utf-8"

    def do_LINK(self):
        self.html = "LINK method response"
        self.content_type = "text/plain; charset=utf-8"

    
    def send_success(self):
        self.handler.send_response(200, "OK")
        self.handler.send_header("Content-type", self.content_type)
        self.handler.end_headers()
        self.handler.wfile.write(self.html.encode())

