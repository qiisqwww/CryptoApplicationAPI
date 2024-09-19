from sqlalchemy.ext.asyncio import AsyncSession

__all__ = [
    "Repository"
]


class Repository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
