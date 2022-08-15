from internal.db_managers.login_db_manager import LoginDBManager


class DBManager:
    login_db_manager: LoginDBManager = None

    @classmethod
    def start(cls):
        cls.login_db_manager = LoginDBManager("./db/accounts.db")

        cls.login_db_manager.start()
