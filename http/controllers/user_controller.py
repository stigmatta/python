from http.server import BaseHTTPRequestHandler

from controllers.controller_rest import ControllerRest

class UserController(ControllerRest):

    def __init__(self, handler: BaseHTTPRequestHandler):
        super().__init__(handler)

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
