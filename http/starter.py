from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import socket
import sys
import urllib.parse

DEV_MODE = True


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
    
    ALLOWED_STATIC_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".css": "text/css",
    ".js": "application/javascript",
    ".html": "text/html",
    }

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
        
        if(self.check_static_asset(parts[0])):
            return
        
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
        
        module_name = self.api["service"].lower() + '_controller'    # назва файлу контролера без розширення (home_controller)
        class_name  = self.api["service"].capitalize() + 'Controller' # назва класу (HomeController)

        # маршрутизація контролерів
        sys.path.append("./")   # додаємо поточну директорію як таку, в якій шукаються модулі динамічного імпорту
        import importlib        # підключаємо інструменти для динамічного імпорту

        try :
            # шукаємо (підключаємо) модуль з іменем module_name
            controller_module = importlib.import_module(f"controllers.{module_name}")
        except Exception as ex:
            self.send_error(404, f"Controller module not found: {module_name} {ex if DEV_MODE else ''}")
            return
        
        # у ньому знаходимо клас class_name, створюємо з нього об'єкт
        controller_class = getattr(controller_module, class_name, None)
        if controller_class is None :
            self.send_error(404, f"Controller class not found: {class_name}")
            return

        controller_object = controller_class(self)
        
        # шукаємо в об'єкті метод serve ...

        mname = 'do_' + self.command
        if not hasattr(controller_object, mname):
            self.send_error(405, "Unsupported method (%r) in '%r'" % (self.command, class_name))
            return
        method = getattr(controller_object, mname)
        # ... та виконуємо його - передаємо управління контролеру

        try :
            method()
        except Exception as ex:
            message = "Request processing error "
            if DEV_MODE : message += str(ex)
            self.send_error(500, message, phrase="Internal server error")
 

    def check_static_asset(self, input: str) -> bool:
        if self.command != "GET":
            return False

        if not input.startswith("/static/"):
            return False

        if input.endswith('/') or '../' in input:
            self.send_error(400, "Invalid static path")
            return True

        relative_path = input.removeprefix("/static/")
        file_path = './http/static/' + relative_path

        ext = os.path.splitext(file_path)[1].lower()

        if ext not in self.ALLOWED_STATIC_TYPES:
            self.send_error(415, "Unsupported Media Type")
            return True

        try:
            with open(file_path, 'rb') as file:
                self.send_response(200, "OK")
                self.send_header("Content-type", self.ALLOWED_STATIC_TYPES[ext])
                self.end_headers()
                self.wfile.write(file.read())
            return True
        except FileNotFoundError:
            self.send_error(404, "Static file not found")
            return True
        except Exception as ex:
            self.send_error(500, "Static file error")
            return True


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
    

