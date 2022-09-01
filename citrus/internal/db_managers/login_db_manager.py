from uuid import uuid4

from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from easydb import StandardDBFactory, Modifier, DataType
from ...utils.encoding import bstring, sbytes

KEY_LENGTH = 16
MEMORY_COST = 2 ** 14
BLOCK_SIZE = 8
PARALLELISATION = 2

SALT_BYTE_LENGTH = 16
ENCODING = "utf-8"

TAG_LENGTH = 6
MAX_TAG_NUMBER = int(TAG_LENGTH * "9")

LOGIN_DETAILS = "LoginDetails"


def encrypt(password: bytes, salt: bytes):
    return scrypt(password, salt, KEY_LENGTH, MEMORY_COST, BLOCK_SIZE, PARALLELISATION)


class LoginDBManager:
    def __init__(self, path):
        self.path = path
        self.db = None

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
        info = info[0] if len(info) > 0 else None

        if info is None:
            return

        correct_password = sbytes(info.get("Password", None))
        salt = sbytes(info.get("Salt", None))

        correct = False

        if salt is not None:
            encrypted_password = encrypt(password.encode(), salt)
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
            salt = get_random_bytes(SALT_BYTE_LENGTH)
            tag = generate_tag(self, username)

            if tag is None:
                return False

            encrypted_password = encrypt(password.encode(), salt)

            self.db.set(LOGIN_DETAILS, data={
                "Username": username,
                "AccountId": account_id,
                "Email": email,
                "Salt": bstring(salt),
                "Password": bstring(encrypted_password),
                "Tag": tag
            })
            self.db.commit()
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
            salt = get_random_bytes(SALT_BYTE_LENGTH)
            encrypted_password = encrypt(new_password.encode(), salt)

            self.db.set(LOGIN_DETAILS, {"AccountId": account_id},
                        {"Salt": bstring(salt), "Password": bstring(encrypted_password)})
            success = True

        return success

    def update_email(self, account_id, new_email):
        success = False

        if not self.account_id_exists(account_id):
            self.db.set(LOGIN_DETAILS, {"AccountId": account_id}, {"Email": new_email})
            success = True

        return success

    def get_account_info(self, account_id):
        info = self.db.get(LOGIN_DETAILS, {"AccountId": account_id}, ["AccountId", "Email", "Username", "Tag"])
        info = info[0] if len(info) > 0 else None

        return {
            "account_id": info.get("AccountId"),
            "email": info.get("Email"),
            "username": info.get("Username"),
            "tag": info.get("Tag")
        } if info is not None else None

    def get_account_id(self, email):
        account_ids = self.db.get(LOGIN_DETAILS, {"Email": email}, ["AccountId"])
        return account_ids[0].get("AccountId", None) if len(account_ids) > 0 else None

    def get_username(self, account_id):
        usernames = self.db.get(LOGIN_DETAILS, {"AccountId": account_id}, ["Username"])
        return usernames[0].get("Username", None) if len(usernames) > 0 else None

    def get_tag(self, account_id):
        tags = self.db.get(LOGIN_DETAILS, {"AccountId": account_id}, ["Tag"])
        return tags[0].get("Tag", None) if len(tags) > 0 else None


def generate_tag(db_manager: LoginDBManager, username):
    tag = len(db_manager.db.get(LOGIN_DETAILS, {"Username": username}, ["Tag"]))

    return f"#{tag:0{TAG_LENGTH}d}" if tag <= MAX_TAG_NUMBER else None


def generate_account_id():
    return uuid4().hex
