from .login_db_manager import LoginDBManager
from ..context_manager import ContextManager


class DBManager:
    login_db_manager: LoginDBManager = None

    @classmethod
    def start(cls):
        if not ContextManager.is_server():
            return

        cls.login_db_manager = LoginDBManager("./db/accounts.db")
        cls.login_db_manager.start()
