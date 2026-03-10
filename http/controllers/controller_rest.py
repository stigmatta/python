from http.server import BaseHTTPRequestHandler

import urllib.parse
from controllers.rest_response import RestResponse, RestStatus
from controllers.rest_error import RestError

class ControllerRest:
    def __init__(self, handler: BaseHTTPRequestHandler):
        self.handler = handler
        self.rest_response = RestResponse()

    def before_execution(self):
        self.rest_response = RestResponse()


    def serve(self):
        self.query_params = {}
        if self.handler.query_string:
            for item in self.handler.query_string.split("&"):
                if not item:
                    continue
                
                key, value = map(lambda input: None if input is None else urllib.parse.unquote_plus(input),
                                  item.split("=", 1) if "=" in item else [item, None])
                
                self.query_params[key] = value if key not in self.query_params else [
                    *(self.query_params[key] if isinstance(self.query_params[key], (list, tuple)) else [self.query_params[key]]),
                    value
                ]
        self.before_execution()
        mname = 'do_' + self.handler.command
        if not hasattr(self, mname):
            self.rest_response.status = RestStatus(
                is_ok=False,
                code=405,
                phrase=f"Unsupported method (%r) in '%r'" % (self.handler.command, self.__class__.__name__)
            )
        else:
            method = getattr(self, mname)

            try:
                method()
                self.send_success()
                return
            except RestError as err:
                self.rest_response.status = RestStatus(
                    is_ok=False,
                    code=err.code,
                    phrase=err.phrase
                )
                self.rest_response.data = err.data
            except Exception as ex:
                message = "Request processing error "
                print(str(ex))
                self.rest_response.status = RestStatus(
                    is_ok=False,
                    code=500,
                    phrase=message + str(ex)
                )
        self.send_error()
    
    def send_success(self):
        self.handler.send_rest_response(self.rest_response)


    def send_error(self):
        self.handler.send_rest_response(self.rest_response)


