import json
from models.request import CgiRequest

class OrderController:
    def __init__(self, request: CgiRequest):
        self.request = request

    def serve(self):
        method = self.request.request_method.lower()
        handler = getattr(self, f"do_{method}", None)
        if handler:
            handler()
        else:
            print("Status: 405 Method Not Allowed")
            print("Content-Type: text/plain\n")
            print(f"Method {method.upper()} not allowed")

    def do_get(self):
        self._respond("GET")

    def do_post(self):
        self._respond("POST")

    def do_put(self):
        self._respond("PUT")

    def do_patch(self):
        self._respond("PATCH")

    def do_delete(self):
        self._respond("DELETE")

    def _respond(self, method_name):
        data = {
            "api": "order",
            "method": method_name
        }
        print("Content-Type: application/json; charset=utf-8")
        print()
        print(json.dumps(data, ensure_ascii=False))
