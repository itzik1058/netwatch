from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class Watcher(ABC):
    @abstractmethod
    async def fetch(self, session: Session) -> None:
        pass
