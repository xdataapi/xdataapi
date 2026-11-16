from enum import StrEnum


class NotFoundReason(StrEnum):
    AGE_RESTRICTED = "age_restricted"
    SUSPENDED = "suspended"
    UNAVAILABLE = "unavailable"

    def __str__(self) -> str:
        return str(self.value)
