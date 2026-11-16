from enum import StrEnum


class NotFoundReason(StrEnum):
    AGE_RESTRICTED = "age_restricted"
    DEACTIVATED = "deactivated"
    SUSPENDED = "suspended"
    UNAVAILABLE = "unavailable"

    def __str__(self) -> str:
        return str(self.value)
