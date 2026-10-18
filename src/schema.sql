PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS Ticket;
DROP TABLE IF EXISTS Trip;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS UserRole;


PRAGMA foreign_keys = ON;

-- Роли
CREATE TABLE UserRole (
    roleID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Пользовалели
CREATE TABLE User (
    passengerID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT,
    password_hash TEXT NOT NULL,
    roleID INTEGER NOT NULL,
    balance DOUBLE DEFAULT 0.0 CHECK (balance >= 0),
    FOREIGN KEY (roleID) REFERENCES UserRole (roleID)
);

-- Рейсы
CREATE TABLE Trip (
    TripID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cost DOUBLE NOT NULL CHECK (cost >= 0),
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    isavaliable BOOLEAN DEFAULT 1,
    description TEXT
);

-- Билеты
CREATE TABLE Ticket (
    TicketID INTEGER PRIMARY KEY AUTOINCREMENT,
    TripID INTEGER NOT NULL,
    passengerID INTEGER NOT NULL,
    statusPayment BOOLEAN DEFAULT 0, -- по умолчанию не оплачено
    start_date DATETIME NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (TripID) REFERENCES Trip (TripID) ON DELETE CASCADE,
    FOREIGN KEY (passengerID) REFERENCES User (passengerID) ON DELETE CASCADE
);


-- Тест

INSERT INTO UserRole (name) VALUES 
('Пассажир'), 
('Кассир');

INSERT INTO User (name, surname, patronymic, password_hash, roleID, balance) VALUES
('Иван', 'Иванов', 'Иванович', 'hash_123', 1, 5000.00),
('Анна', 'Петрова', 'Сергеевна', 'hash_123', 1, 1500.50),
('Пётр', 'Сидоров', 'Петрович', 'hash_admin', 2, 0.00);

INSERT INTO Trip (name, cost, start_date, end_date, isavaliable, description) VALUES
('НН - Москва', 1500.00, '2026-11-01 08:30', '2026-11-01 14:00', 1, 'Комфортабельный автобус'),
('НН - Казань', 1200.00, '2026-11-02 09:15', '2026-11-02 15:30', 1, 'Есть Wi-Fi'),
('Москва - СПб', 2500.00, '2026-11-03 07:00', '2026-11-03 12:00', 1, 'Скоростной экспресс');

INSERT INTO Ticket (TripID, passengerID, statusPayment) VALUES
(1, 1, 1), -- Иванов купил билет на рейс 1 (оплачен)
(1, 2, 1), -- Петрова купила билет на рейс 1 (оплачен)
(3, 1, 0); -- Иванов забронировал билет на рейс 3 (не оплачен)