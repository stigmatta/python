from controllers.controller_rest import RestController, RestMeta, RestCache


class DiscountController(RestController):

    def serve(self):
        self.response.meta = RestMeta(
           service="Discount API",
           links={
               "get": "GET /discount",
               "post": "POST /discount",
           }
        )
        super().serve()

    def do_get(self):
        self.response.meta.service += ": User`s bonuses"
        self.response.meta.cache = RestCache.hrs1
        self.response.data = {
            "int": 10,
            "float": 1e-3,
            "str": "GET",
            "cyr": "Привіт",
            "headers": self.request.headers,
        }

    def do_post(self):
        self.response.meta.service += ": post"
        self.response.meta.data_type = "object"
        self.response.data = {
            "int": 10,
            "float": 1e-3,
            "str": "POST",
            "cyr": "Привіт",
            "headers": self.request.headers,
        }