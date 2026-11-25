DROP TABLE IF EXISTS Ticket;
DROP TABLE IF EXISTS Trip;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS UserRole;

CREATE TABLE UserRole (
    roleID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE User (
    passengerID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT,
    login TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    roleID INTEGER NOT NULL,
    balance REAL NOT NULL DEFAULT 0,
    FOREIGN KEY (roleID) REFERENCES UserRole (roleID)
);

CREATE TABLE Trip (
    TripID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cost REAL NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    seats INTEGER NOT NULL DEFAULT 0,
    isavaliable INTEGER NOT NULL DEFAULT 1,
    description TEXT
);

CREATE TABLE Ticket (
    TicketID INTEGER PRIMARY KEY AUTOINCREMENT,
    TripID INTEGER NOT NULL,
    passengerID INTEGER NOT NULL,
    statusPayment INTEGER NOT NULL DEFAULT 0,
    start_date TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (TripID) REFERENCES Trip (TripID),
    FOREIGN KEY (passengerID) REFERENCES User (passengerID)
);

INSERT INTO UserRole (name)
VALUES ('Passenger'), ('Cashier');


-- Тестовые пользователи (пароль у всех: 123)
INSERT INTO User (name, surname, patronymic, login, password_hash, roleID, balance) VALUES
('Иван', 'Иванов', 'Иванович', 'ivan', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1, 5000.00),
('Анна', 'Петрова', 'Сергеевна', 'anna', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1, 1500.50);

INSERT INTO Trip (name, cost, start_date, end_date, seats, isavaliable, description) VALUES
('НН - Москва', 1500.00, '2026-11-01 08:30', '2026-11-01 14:00', 40, 1, 'Комфортабельный автобус'),
('Москва - СПб', 2000.00, '2026-11-02 09:00', '2026-11-02 18:00', 30, 1, 'Скоростной поезд'),
('СПб - Казань', 1800.00, '2026-11-03 10:00', '2026-11-03 20:00', 20, 1, 'Автобус с Wi-Fi');

INSERT INTO Ticket (TripID, passengerID, statusPayment) VALUES
(1, 1, 1), -- Иванов купил билет на рейс 1 (оплачен)
(1, 2, 1), -- Петрова купила билет на рейс 1 (оплачен)
(3, 1, 0); -- Иванов забронировал билет на рейс 3 (не оплачен)