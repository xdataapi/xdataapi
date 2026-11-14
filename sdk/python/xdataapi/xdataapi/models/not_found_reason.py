from enum import StrEnum


class NotFoundReason(StrEnum):
    SUSPENDED = "suspended"
    UNAVAILABLE = "unavailable"

    def __str__(self) -> str:
        return str(self.value)
