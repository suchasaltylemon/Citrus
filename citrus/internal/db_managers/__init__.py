from .login_db_manager import LoginDBManager
from ..lifecycle_manager import LifecycleManager


class DBManager:
    login_db_manager: LoginDBManager = None

    @classmethod
    def start(cls):
        if not LifecycleManager.is_server():
            return

        cls.login_db_manager = LoginDBManager("./db/accounts.db")
        cls.login_db_manager.start()
