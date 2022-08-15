from citrus import export
from citrus.core.controller import controller
from citrus.lifecycle import onstart


@onstart()
@controller()
class HelloWorldController:
    def on_start(self):
        print("Hello, World")


export(HelloWorldController)
