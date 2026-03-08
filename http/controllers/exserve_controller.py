from controllers.controller_rest import ControllerRest


class ExserveController(ControllerRest):
    def serve(self):
        raise Exception("Test exception in serve() method")