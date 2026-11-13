from dataclasses import dataclass

@dataclass
class User:
    passengerID: int
    name: str
    surname: str
    patronymic: str | None = None
    password_hash: str
    roleID: int
    balance: float

    role_name: str | None = None
#?
    def get_full_name(self) -> str:
        patronymic = f" {self.patronymic}" if self.patronymic else ""
        return f"{self.surname} {self.name}{patronymic}"