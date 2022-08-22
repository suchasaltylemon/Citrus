from .login_db_manager import LoginDBManager
from ..runtime_manager import RuntimeManager


class DBManager:
    login_db_manager: LoginDBManager = None

    @classmethod
    def start(cls):
        if not RuntimeManager.is_server():
            return

        cls.login_db_manager = LoginDBManager("./db/accounts.db")
        cls.login_db_manager.start()
