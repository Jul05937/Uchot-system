from src.system.repositories import user_repository
from src.system.services import user_service

def authenticate(login_value: str, password_value: str):
    try:
        user = user_repository.get_by_id(int(login_value))
        if user and user.password_hash == password_value:
            return user
    except ValueError:
        pass
    return None

def login():
    print("\n=== Вход в систему ===")
    login_value = input("Введите ваш ID (логин): ")
    password_value = input("Введите пароль: ")
    
    user = authenticate(login_value, password_value)
    if not user:
        print("Ошибка: Неверный ID или пароль!")
        return None
    
    print(f"Добро пожаловать, {user.get_full_name()}!")
    return user

def register():
    print("\n=== Регистрация пассажира ===")
    name = input("Имя: ")
    surname = input("Фамилия: ")
    patronymic = input("Отчество (или Enter, если нет): ")
    password = input("Придумайте пароль: ")
    
    try:
        user_service.register_user(name, surname, patronymic, 0, password, role_id=1)
        print("Регистрация прошла успешно! Теперь вы можете войти.")
    except Exception as e:
        print(f"Ошибка регистрации: {e}")