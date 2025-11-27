from models.request import CgiRequest

class HomeController:

    def __init__(self, request: CgiRequest):
        self.request = request

    def serve(self):
        action = (
            self.request.path_parts[1].lower()
            if len(self.request.path_parts) > 1 and len(self.request.path_parts[1].strip()) > 0
            else 'index'
        )
        controller_action = getattr(self, action)
        controller_action()

    def index(self):
        print("Content-Type: text/html; charset=utf-8\n")
        print()

        html = """<!DOCTYPE html>
        <html lang="uk">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AM-CGI</title>
            <link rel="icon" href="/img/python.png" />
            <link rel="stylesheet" href="/css/site.css" />
        </head>
        <body>
        <h1>Головна сторінка</h1>
        <ul>
            <li><a href="/home/privacy">Політика конфіденційності</a></li>
            <li><a href="/home/params">Всі параметри від диспетчера доступу</a></li>
        </ul>
        <img src="/img/Python.png" width="100" />
        <img src="/img/m13.jpg" width="100" />
        <script src="/js/site.js"></script>
        </body>
        </html>
        """

        print(html)

    def privacy(self):
        print("Content-Type: text/html; charset=utf-8\n")
        print()

        html = """<!DOCTYPE html>
        <html lang="uk">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AM-CGI - Privacy</title>
            <link rel="icon" href="/img/python.png" />
            <link rel="stylesheet" href="/css/site.css" />
        </head>
        <body>
        <h1>Політика конфіденційності</h1>
        <p>
            Згідно з принципів CGI всі параметри від сервера (Apache) до скрипту
            передаються як змінні оточення.
        </p>
        </body>
        </html>
        """

        print(html)

    def params(self):
        print("Content-Type: text/html; charset=utf-8\n")
        print()

        envs = "<ul>\n" + "".join(f"<li>{k} = {v}</li>\n" for k, v in self.request.server.items()) + "</ul>\n"
        hdrs = "<ul>\n" + "".join(f"<li>{k} = {v}</li>\n" for k, v in self.request.headers.items()) + "</ul>\n"
        qp = "<ul>\n" + "".join(f"<li>{k} = {v}</li>\n" for k, v in self.request.query_params.items()) + "</ul>\n"

        html = f"""<!DOCTYPE html>
        <html lang="uk">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AM-CGI - Params</title>
            <link rel="icon" href="/img/python.png" />
            <link rel="stylesheet" href="/css/site.css" />
        </head>
        <body>
        <h1>Всі параметри від диспетчера доступу</h1>
        <p><a href="/home/index">На головну</a></p>
        <h2>Змінні оточення</h2>
        {envs}
        <h2>Заголовки</h2>
        {hdrs}
        <h2>Параметри запиту</h2>
        {qp}
        </body>
        </html>
        """

        print(html)
