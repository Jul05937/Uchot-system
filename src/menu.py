from src.system.services import ticket_service, trip_service
from src.system.repositories import trip_repository, user_repository

def passenger_menu(user):
    while True:
        print(f"\n===== МЕНЮ ПАССАЖИРА ({user.get_full_name()}) =====")
        print(f"Ваш баланс: {user.balance} руб.")
        print("1. Посмотреть доступные рейсы")
        print("2. Купить билет")
        print("3. Мои билеты (история поездок)")
        print("4. Вернуть билет")
        print("0. Выйти из аккаунта")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            trips = trip_repository.get_all()
            print("\n--- Доступные рейсы ---")
            for t in trips:
                status = "Есть места" if t.isavaliable else "Мест нет"
                print(f"ID: {t.TripID} | {t.name} | {t.start_date} | Цена: {t.cost} | {status}")
                
        elif choice == "2":
            try:
                trip_id = int(input("Введите ID рейса для покупки: "))
                ticket_service.buy_ticket(user.passengerID, trip_id)
                user = user_repository.get_by_id(user.passengerID) 
            except Exception as e:
                print(f"Ошибка: {e}")
                
        elif choice == "3":
            try:
                tickets = ticket_service.get_user_tickets(user.passengerID)
                print("\n--- Ваши билеты ---")
                for t in tickets:
                    status = "Оплачен" if t.statusPayment else "Возвращен/Не оплачен"
                    print(f"ID билета: {t.TicketID} | Рейс ID: {t.TripID} | Статус: {status} | Дата: {t.start_date}")
            except Exception as e:
                print(f"Ошибка: {e}")
                
        elif choice == "4":
            try:
                ticket_id = int(input("Введите ID билета для возврата: "))
                ticket_service.return_ticket(ticket_id)
                user = user_repository.get_by_id(user.passengerID)
            except Exception as e:
                print(f"Ошибка: {e}")
                
        elif choice == "0":
            print("Выход из аккаунта...")
            break

def cashier_menu(user):
    while True:
        print(f"\n===== МЕНЮ КАССИРА ({user.get_full_name()}) =====")
        print("1. Добавить новый рейс")
        print("2. Посмотреть все рейсы")
        print("0. Выйти из аккаунта")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            try:
                name = input("Название рейса (например, НН-Москва): ")
                cost = float(input("Цена билета: "))
                start_date = input("Дата и время отправления (ГГГГ-ММ-ДД ЧЧ:ММ): ")
                end_date = input("Дата и время прибытия (ГГГГ-ММ-ДД ЧЧ:ММ): ")
                description = input("Описание (необязательно): ")
                
                trip_service.create_trip(user.passengerID, name, cost, start_date, end_date, description)
            except Exception as e:
                print(f"Ошибка: {e}")
            except ValueError:
                print("Ошибка: Цена должна быть числом!")
                
        elif choice == "2":
            trips = trip_repository.get_all()
            print("\n--- Все рейсы ---")
            for t in trips:
                print(f"ID: {t.TripID} | {t.name} | Цена: {t.cost} | {t.start_date}")
                
        elif choice == "0":
            print("Выход из аккаунта...")
            break