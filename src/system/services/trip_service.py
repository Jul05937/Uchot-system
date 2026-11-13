from src.system.repositories import trip_repository, user_repository

CASHIER_ROLE_ID = 2

def create_trip(cashier_id: int, name: str, cost: float, start_date: str, end_date: str, description: str = None):
    user = user_repository.get_by_id(cashier_id)
    if not user:
        raise Exception("Пользователь не найден")
    if user.roleID != CASHIER_ROLE_ID:
        raise Exception("Только кассир может добавлять новые рейсы")

    if not name.strip():
        raise Exception("Название рейса не может быть пустым")
    if cost <= 0:
        raise Exception("Стоимость билета должна быть больше нуля")
    if not start_date or not end_date:
        raise Exception("Укажите дату и время отправления и прибытия")

    trip_repository.create(name, cost, start_date, end_date, description)
    print(f"Рейс '{name}' успешно добавлен!")