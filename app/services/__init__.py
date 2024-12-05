from abc import ABC

from core.db.repository import DatabaseRepository
from core.db.uow import get_uow


class Service(ABC):
    def __init__(self, repo: DatabaseRepository):
        self.repo = repo
        self.uow = get_uow(repo.session)
