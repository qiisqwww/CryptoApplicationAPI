from enum import StrEnum, verify, UNIQUE

__all__ = [
    "TokenType"
]


@verify(UNIQUE)
class TokenType(StrEnum):
    FIELD = "type"
    ACCESS = "access"
    REFRESH = "refresh"
