from src.database import init_db
from src.auth import login, register
from src.menu import passenger_menu, cashier_menu
from src.system.services.auth_service import create_default_admin

def main():
    try:
        init_db()
    except Exception as e:
        print(f"Ошибка инициализации БД: {e}")
        return
    create_default_admin()
    
    print("Добро пожаловать в систему учёта пассажиров и поездок!")
    while True:
        print("\n=== ГЛАВНОЕ МЕНЮ ===")
        print("1. Войти в систему")
        print("2. Зарегистрироваться (для пассажиров)")
        print("0. Выйти из программы")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            user = login()
            if user:
                if user.roleID == 1:
                    passenger_menu(user)
                elif user.roleID == 2:
                    cashier_menu(user)
                else:
                    print("Неизвестная роль пользователя!")
                    
        elif choice == "2":
            register()
            
        elif choice == "0":
            print("До свидания!")
            break

if __name__ == "__main__":
    main()