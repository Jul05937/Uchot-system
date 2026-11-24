import hashlib
from src.system.repositories import user_repository
from src.system.models.user import User

PASSENGER_ROLE_ID = 1
CASHIER_ROLE_ID = 2

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(login_value: str, password_value: str) -> User | None:
    user = user_repository.get_by_login(login_value)
    if not user:
        return None
    if user.password_hash != hash_password(password_value):
        return None
    return user

def register_passenger(name: str, surname: str, patronymic: str | None, login_value: str, password_value: str):
    if user_repository.get_by_login(login_value):
        raise Exception("Пользователь уже существует")
    user_repository.create(
        name=name,
        surname=surname,
        patronymic=patronymic,
        login=login_value,
        password_hash=hash_password(password_value),
        roleID=PASSENGER_ROLE_ID
    )

def register_cashier(name: str, surname: str, patronymic: str | None, login_value: str, password_value: str):
    if user_repository.get_by_login(login_value):
        raise Exception("Пользователь уже существует")
    user_repository.create(
        name=name,
        surname=surname,
        patronymic=patronymic,
        login=login_value,
        password_hash=hash_password(password_value),
        roleID=CASHIER_ROLE_ID
    )

def create_default_admin():
    if user_repository.get_by_login("admin"):
        return
    user_repository.create(
        name="System",
        surname="Admin",
        patronymic=None,
        login="admin",
        password_hash=hash_password("admin"),
        roleID=CASHIER_ROLE_ID
    )