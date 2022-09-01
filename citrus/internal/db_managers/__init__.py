from .login_db_manager import LoginDBManager
from ..context_manager import ContextManager
from ..singleton import singleton
from ...include.signalio import LOADER

context_manager = ContextManager()


@singleton
class DBManager:
    login_db_manager: LoginDBManager = None

    def start(self):
        if not context_manager.is_server():
            return

        self.login_db_manager = LoginDBManager("./db/accounts.db")
        self.login_db_manager.start()
