from citrus import export
from citrus.core import login, signup
from citrus.core.controller import controller
from citrus.lifecycle import onstart


@controller()
@onstart()
class LoginController:
    def on_start(self):
        should_login = input("Login?\n y/n: ").lower().strip() == "y"

        email = input("Email: ").strip().lower()
        password = input("Password: ").strip()

        if should_login:
            info = login(email, password)
            print(info)

        else:
            username = input("Username: ").strip()

            signup(email, username, password)


export(LoginController)
