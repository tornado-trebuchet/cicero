from datetime import date as _date
from datetime import datetime as _datetime
from datetime import timezone as _timezone
from urllib.parse import urlparse
from uuid import UUID as _UUID

from src.domain.models.base_vo import ValueObject


class UUID(ValueObject):
    __slots__ = ("_value",)

    def __init__(self, value: str | _UUID):
        if isinstance(value, _UUID):
            self._value = value
        else:
            value = value.strip()
            if not value:
                raise ValueError("UUID cannot be empty.")
            try:
                self._value = _UUID(value)
            except Exception:
                raise ValueError(f"Invalid UUID: {value}")

    @property
    def value(self) -> _UUID:
        return self._value

    @staticmethod
    def new() -> "UUID":
        import uuid

        return UUID(uuid.uuid4())

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, UUID):
            return self._value == other._value
        return False

    def __hash__(self) -> int:
        return hash(self._value)


class DateTime(ValueObject):
    __slots__ = ("_value",)

    def __init__(self, value: _datetime | _date | str):
        if isinstance(value, _datetime):
            self._value = value
        elif isinstance(value, _date):
            # Convert date to datetime at midnight
            self._value = _datetime.combine(value, _datetime.min.time())
        elif type(value) is str:
            try:
                self._value = _datetime.fromisoformat(value)
            except ValueError:
                raise ValueError(f"Invalid ISO datetime string: {value}")
        else:
            raise ValueError(
                "DateTime must be a datetime, date, or ISO string."
            )

    @property
    def value(self) -> _datetime:
        return self._value

    @classmethod
    def now(cls) -> "DateTime":
        return cls(_datetime.now(_timezone.utc))

    @classmethod
    def from_timestamp(cls, ts: float) -> "DateTime":
        return cls(_datetime.fromtimestamp(ts, _timezone.utc))

    def to_timestamp(self) -> float:
        return self._value.timestamp()

    def to_iso(self) -> str:
        return self._value.isoformat()

    def to_date(self) -> str:
        return self._value.date().isoformat()

    def __str__(self) -> str:
        return self._value.isoformat()


class HttpUrl(ValueObject):
    __slots__ = ("_value",)

    def __init__(self, value: str):
        value = value.strip()
        if not value:
            raise ValueError("URL cannot be empty.")
        parsed = urlparse(value)
        if not (parsed.scheme and parsed.netloc):
            raise ValueError(f"Invalid URL: {value}")
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value
