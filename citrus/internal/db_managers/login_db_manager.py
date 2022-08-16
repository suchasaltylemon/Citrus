import random
import secrets
import string
from hashlib import sha256
from uuid import uuid4

from include.easydb import StandardDBFactory, Modifier, DataType, DB

SALT_BYTE_LENGTH = 8
ENCODING = "utf-8"
TAG_LENGTH = 6

MAX_TAG_ITERATIONS = 2048

LOGIN_DETAILS = "LoginDetails"


def generate_salt():
    return secrets.token_hex(SALT_BYTE_LENGTH)


def generate_account_id():
    return uuid4().hex


def encrypt(password, salt):
    salted = password + salt

    return sha256(salted.encode(ENCODING))


def generate_tag(username):
    tag = None
    iterations = 0

    while tag is None and iterations < MAX_TAG_ITERATIONS:
        tag = f"#{''.join([random.choice(string.digits) for _ in range(TAG_LENGTH)])}" if not LoginDBManager.db.has(
            LOGIN_DETAILS, {"Username": username, "Tag": tag}) else None

    return tag


class LoginDBManager:
    db: DB = None

    def __init__(self, path):
        self.path = path

    def init_tables(self):
        if not self.db.table_exists(LOGIN_DETAILS):
            self.db.create_table(LOGIN_DETAILS, {
                "AccountId": [DataType.String, [Modifier.Unique, Modifier.NotNull, Modifier.PrimaryKey]],
                "Username": [DataType.String, [Modifier.NotNull]],
                "Email": [DataType.String, [Modifier.Unique, Modifier.Unique]],
                "Password": [DataType.String, [Modifier.NotNull]],
                "Salt": [DataType.String, [Modifier.NotNull]],
                "Tag": [DataType.String, [Modifier.NotNull]]
            })

    def start(self):
        self.db = StandardDBFactory.create_db(self.path)

        self.init_tables()

    def verify_login(self, email, password):
        info = self.db.get(LOGIN_DETAILS, {"Email": email}, ["Salt", "Password"])

        correct_password = info.get("Password", None)
        salt = info.get("Salt", None)

        correct = False

        if salt is not None:
            encrypted_password = encrypt(password, salt)
            correct = encrypted_password == correct_password

        return correct

    def account_exists(self, email):
        return self.db.has(LOGIN_DETAILS, {"Email": email})

    def account_id_exists(self, account_id):
        return self.db.has(LOGIN_DETAILS, {"AccountId": account_id})

    def create_account(self, email, username, password):
        success = False

        if not self.account_exists(email):
            account_id = generate_account_id()
            salt = generate_salt()
            tag = generate_tag(username)

            if tag is None:
                return False

            encrypted_password = encrypt(password, salt)

            self.db.set(LOGIN_DETAILS, data={
                "Username": username,
                "AccountId": account_id,
                "Email": email,
                "Salt": salt,
                "Password": encrypted_password,
                "Tag": tag
            })
            success = True

        return success

    def update_username(self, account_id, new_username):
        success = False

        if not self.account_id_exists(account_id):
            self.db.set(LOGIN_DETAILS, {"AccountId": account_id}, {"Username": new_username})
            success = True

        return success

    def update_password(self, account_id, new_password):
        success = False

        if not self.account_id_exists(account_id):
            salt = generate_salt()
            encrypted_password = encrypt(new_password, salt)

            self.db.set(LOGIN_DETAILS, {"AccountId": account_id}, {"Salt": salt, "Password": encrypted_password})
            success = True

        return success

    def update_email(self, account_id, new_email):
        success = False

        if not self.account_id_exists(account_id):
            self.db.set(LOGIN_DETAILS, {"AccountId": account_id}, {"Email": new_email})
            success = True

        return success

    def get_account_id(self, email):
        return self.db.get(LOGIN_DETAILS, {"Email": email}, ["AccountId"]).get("AccountId", None)

    def get_username(self, account_id):
        return self.db.get(LOGIN_DETAILS, {"AccountId": account_id}, ["Username"]).get("Username", None)

    def get_tag(self, account_id):
        return self.db.get(LOGIN_DETAILS, {"AccountId": account_id}, ["Tag"]).get("Tag", None)
