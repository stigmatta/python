from http.server import BaseHTTPRequestHandler

from controllers.controller_rest import ControllerRest
from controllers.rest_error import RestError

class UserController(ControllerRest):

    def do_GET(self):
        self.rest_response.data = {
            "x": 10,
            "y": 20,
            "z": 30,
            "w": 40,
            "hello": "world",
            "query_params": self.handler.query_params,
            "api": self.handler.api
        }

    def do_POST(self):
        raise RestError(code=422, phrase="Unprocessable Entity", data="Invalid format for email")
