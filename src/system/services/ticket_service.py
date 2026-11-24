from src.system.repositories import ticket_repository, trip_repository, user_repository

PASSENGER_ROLE_ID = 1
CASHIER_ROLE_ID = 2

def buy_ticket(passenger_id: int, trip_id: int) -> None:
    user = user_repository.get_by_id(passenger_id)
    if not user:
        raise Exception("Пассажир не найден")
    if user.roleID != PASSENGER_ROLE_ID:
        raise Exception("Только пассажир может покупать билет")

    trip = trip_repository.get_by_id(trip_id)
    if not trip:
        raise Exception("Рейс не найден")
    if not trip.isavaliable:
        raise Exception("Рейс недоступен")

    bought = ticket_repository.count_active_by_trip(trip_id)
    if bought >= trip.seats:
        raise Exception("На этот рейс больше нет свободных мест")

    if user.balance < trip.cost:
        raise Exception(f"Недостаточно средств. Баланс: {user.balance}, цена билета: {trip.cost}")

    new_balance = user.balance - trip.cost
    user_repository.update_balance(passenger_id, new_balance)

    ticket_repository.create(trip_id, passenger_id, status_payment=True)

    print("Билет успешно куплен!")

def return_ticket(ticket_id: int, cashier_id: int) -> None:
    cashier = user_repository.get_by_id(cashier_id)
    if not cashier or cashier.roleID != CASHIER_ROLE_ID:
        raise Exception("Только кассир может принимать возврат")

    ticket = ticket_repository.get_by_id(ticket_id)
    if not ticket:
        raise Exception("Билет не найден")
    if not ticket.statusPayment:
        raise Exception("Билет уже возвращен или не был оплачен")

    trip = trip_repository.get_by_id(ticket.TripID)
    user = user_repository.get_by_id(ticket.passengerID)
    if not trip or not user:
        raise Exception("Ошибка данных: рейс или пассажир не найдены")

    new_balance = user.balance + trip.cost
    user_repository.update_balance(user.passengerID, new_balance)
    ticket_repository.update_status(ticket_id, status_payment=False)

    print(f"Билет успешно возвращен. Деньги ({trip.cost}) зачислены на баланс.")

def cancel_ticket(ticket_id: int, passenger_id: int) -> None:
    ticket = ticket_repository.get_by_id(ticket_id)
    if not ticket:
        raise Exception("Билет не найден")
    if ticket.passengerID != passenger_id:
        raise Exception("Нельзя вернуть чужой билет")
    if not ticket.statusPayment:
        raise Exception("Билет уже возвращен или не был оплачен")

    trip = trip_repository.get_by_id(ticket.TripID)
    user = user_repository.get_by_id(ticket.passengerID)
    if not trip or not user:
        raise Exception("Ошибка данных: рейс или пассажир не найдены")

    new_balance = user.balance + trip.cost
    user_repository.update_balance(user.passengerID, new_balance)
    ticket_repository.update_status(ticket_id, status_payment=False)

    print(f"Билет успешно возвращен. Деньги ({trip.cost}) зачислены на баланс.")

def get_user_tickets(passenger_id: int) -> list:
    user = user_repository.get_by_id(passenger_id)
    if not user:
        raise Exception("Пользователь не найден")
    return ticket_repository.get_by_passenger(passenger_id)