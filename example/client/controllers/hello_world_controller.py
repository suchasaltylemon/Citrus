from lib import export
from lib.core.controller import controller
from lib.lifecycle import onstart


@onstart()
@controller()
class HelloWorldController:
    def on_start(self):
        print("Hello, World")


export(HelloWorldController)
