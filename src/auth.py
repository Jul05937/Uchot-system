from src.system.services.auth_service import (
    authenticate,
    register_passenger,
    register_cashier
)

def login():
    print("\n=== Вход в систему ===")
    login_value = input("Логин: ")
    password_value = input("Пароль: ")

    user = authenticate(login_value, password_value)
    if not user:
        print("Ошибка: Неверный логин или пароль!")
        return None

    print(f"Добро пожаловать, {user.get_full_name()}!")
    return user

def register():
    print("\n=== Регистрация пассажира ===")
    name = input("Имя: ")
    surname = input("Фамилия: ")
    patronymic = input("Отчество (или Enter, если нет): ")
    login_value = input("Логин: ")
    password_value = input("Пароль: ")

    try:
        register_passenger(name, surname, patronymic, login_value, password_value)
        print("Регистрация прошла успешно! Теперь вы можете войти.")
    except Exception as e:
        print(f"Ошибка регистрации: {e}")

def register_cashier_ui():
    print("\n=== Регистрация кассира ===")
    name = input("Имя: ")
    surname = input("Фамилия: ")
    patronymic = input("Отчество (или Enter, если нет): ")
    login_value = input("Логин: ")
    password_value = input("Пароль: ")

    try:
        register_cashier(name, surname, patronymic, login_value, password_value)
        print("Кассир создан.")
    except Exception as e:
        print(f"Ошибка регистрации: {e}")