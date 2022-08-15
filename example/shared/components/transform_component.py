from citrus import export
from citrus.core.component import component
from citrus.lifecycle import onstart


@onstart()
@component()
class Transform:
    X = 0
    Y = 0


export(Transform)
