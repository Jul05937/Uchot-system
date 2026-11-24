from src.system.repositories import trip_repository, user_repository
from datetime import datetime

CASHIER_ROLE_ID = 2
DATE_FORMAT = "%Y-%m-%d %H:%M"

def create_trip(cashier_id: int, name: str, cost: float, seats: int, start_date: str, end_date: str, description: str = None):
    user = user_repository.get_by_id(cashier_id)
    if not user:
        raise Exception("Пользователь не найден")
    if user.roleID != CASHIER_ROLE_ID:
        raise Exception("Только кассир может добавлять новые рейсы")

    if not name.strip():
        raise Exception("Название рейса не может быть пустым")
    if cost <= 0:
        raise Exception("Стоимость билета должна быть больше нуля")
    if seats <= 0:
        raise Exception("Количество мест должно быть больше нуля")

    try:
        start_dt = datetime.strptime(start_date, DATE_FORMAT)
        end_dt = datetime.strptime(end_date, DATE_FORMAT)
    except ValueError:
        raise Exception("Дата должна быть в формате ГГГГ-ММ-ДД ЧЧ:ММ")

    if end_dt <= start_dt:
        raise Exception("Дата прибытия должна быть позже даты отправления")

    trip_repository.create(name, cost, start_date, end_date, seats, description)
    print(f"Рейс '{name}' успешно добавлен!")