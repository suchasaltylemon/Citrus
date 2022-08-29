from citrus import export
from citrus.core.service import service
from citrus.lifecycle import onstart


@service()
@onstart()
class ExampleService:
    def on_start(self):
        pass


export(ExampleService)
