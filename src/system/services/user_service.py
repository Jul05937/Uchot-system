from src.system.repositories import user_repository
from src.system.models.user import User

def get_user_by_id(passenger_id: int) -> User:
    user = user_repository.get_by_id(passenger_id)
    if not user:
        raise Exception(f"Пользователь с ID {passenger_id} не найден")
    return user