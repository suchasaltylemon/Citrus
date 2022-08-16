from internal.endpoints.client import send_to_server


def _treat_password(password):
    return password


def login(email, password):
    treated = _treat_password(password)


def signup(email, username, password):
    treated = _treat_password(password)

    send_to_server("__signup", {
        "Email": email,
        "Username": username,
        "Password": treated
    })
