from src.system.repositories import user_repository
from src.system.models.user import User

def register_user(name: str, surname: str, patronymic: str, login_or_id: int, password_hash: str, role_id: int) -> User:
    if not name.strip():
        raise Exception("Имя не может быть пустым")
    if not surname.strip():
        raise Exception("Фамилия не может быть пустой")
    
    users = user_repository.get_all()
    for u in users:
        if (u.name.lower() == name.lower() and 
            u.surname.lower() == surname.lower() and 
            (u.patronymic or "").lower() == (patronymic or "").lower()):
            raise Exception("Пользователь с таким ФИО уже существует")

    user_repository.create(name, surname, patronymic, password_hash, role_id)
    return None 

def get_user_by_id(passenger_id: int) -> User:
    user = user_repository.get_by_id(passenger_id)
    if not user:
        raise Exception(f"Пользователь с ID {passenger_id} не найден")
    return user