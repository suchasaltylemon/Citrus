from core.component import component


@component()
class Networkable:
    _connection = None

    def set_connection(self, connection_object):
        self._connection = connection_object

    def get_connection(self):
        return self._connection
