from dataclasses import dataclass

@dataclass
class User:
    passengerID: int
    name: str
    surname: str
    login: str
    password_hash: str
    roleID: int
    balance: float
    patronymic: str | None = None
    role_name: str | None = None

    def get_full_name(self) -> str:
        patronymic = f" {self.patronymic}" if self.patronymic else ""
        return f"{self.surname} {self.name}{patronymic}"