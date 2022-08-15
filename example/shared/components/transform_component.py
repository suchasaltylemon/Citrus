from lib import export
from lib.core.component import component
from lib.lifecycle import onstart


@onstart()
@component()
class Transform:
    X = 0
    Y = 0


export(Transform)
