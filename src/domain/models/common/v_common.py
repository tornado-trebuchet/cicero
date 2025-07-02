from uuid import UUID as _UUID
from datetime import datetime as _datetime, timezone as _timezone
from urllib.parse import urlparse
from src.domain.models.common.base_model import ValueObject

class UUID(ValueObject):
    __slots__ = ("_value",)

    def __init__(self, value: str | _UUID):
        if isinstance(value, _UUID):
            self._value = value
        elif isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("UUID cannot be empty.")
            try:
                self._value = _UUID(value)
            except Exception:
                raise ValueError(f"Invalid UUID: {value}")
        else:
            raise ValueError("UUID must be a string or uuid.UUID instance.")

    @property
    def value(self) -> _UUID:
        return self._value

    @staticmethod
    def new() -> "UUID":
        import uuid
        return UUID(uuid.uuid4())

    def __str__(self) -> str:
        return str(self._value)
    

class DateTime(ValueObject):
    __slots__ = ("_value",)

    def __init__(self, value: _datetime | str):
        if isinstance(value, _datetime):
            self._value = value
        elif isinstance(value, str):
            try:
                self._value = _datetime.fromisoformat(value)
            except ValueError:
                raise ValueError(f"Invalid ISO datetime string: {value}")
        else:
            raise ValueError("DateTime must be a datetime or ISO string.")

    @classmethod
    def now(cls) -> "DateTime":
        return cls(_datetime.now(_timezone.utc))

    @classmethod
    def from_timestamp(cls, ts: float) -> "DateTime":
        return cls(_datetime.fromtimestamp(ts, _timezone.utc))

    @property
    def value(self) -> _datetime:
        return self._value

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


        