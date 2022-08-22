from ...core.component import component, Component


@component()
class Networkable(Component):
    _connection = None
    _session_token = None

    def set_session_token(self, session_token):
        self._session_token = session_token

    def get_session_token(self):
        return self._session_token

    def set_connection(self, connection_object):
        self._connection = connection_object

    def get_connection(self):
        return self._connection
