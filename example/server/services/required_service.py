from citrus import export
from citrus.core.service import service


@service()
class RequiredService:
    pass


export(RequiredService)
