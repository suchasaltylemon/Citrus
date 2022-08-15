from citrus.lifecycle import ON_START, ON_START_REGISTERED

SERVER_CONTEXT = "server"
CLIENT_CONTEXT = "client"


class RuntimeManager:
    services = []
    controllers = []

    started = False

    context = None

    @classmethod
    def register_service(cls, service_object):
        assert cls.context != CLIENT_CONTEXT, "Runtime is running as client! Cannot register any services!"

        cls.context = SERVER_CONTEXT
        cls.services.append(service_object)

    @classmethod
    def register_controller(cls, controller_object):
        assert cls.context != SERVER_CONTEXT, "Runtime is running as server! Cannot register any " \
                                              "controllers! "

        cls.context = CLIENT_CONTEXT
        cls.controllers.append(controller_object)

    @classmethod
    def start(cls):
        for service in cls.services:
            if hasattr(service, ON_START_REGISTERED):
                assert hasattr(service,
                               ON_START), "Service has subscribed to 'on_start' lifecycle, but has not implemented " \
                                          "method "

                getattr(service, ON_START)()

        for controller in cls.controllers:
            if hasattr(controller, ON_START_REGISTERED):
                assert hasattr(controller,
                               ON_START), "Controller has subscribed to 'on_start' lifecycle, but has not" + \
                                          " implemented method"

                getattr(controller, ON_START)()

        cls.started = True
