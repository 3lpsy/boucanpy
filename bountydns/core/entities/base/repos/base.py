from typing import Optional, List
from fastapi import Depends
from sqlalchemy.orm import Session
from bountydns.db.session import session
from bountydns.db.pagination import Pagination
from bountydns.core.entities.pagination.responses import PaginationData


class BaseRepo:
    model = None

    def __init__(self, db: Session = Depends(session)):
        self.db = db

    def get(self, id) -> Optional[model]:
        return self.query().get(id)

    def all(self) -> List[model]:
        return self.query().all()

    def paginate(self, pagination):
        results = self.query().paginate(
            page=pagination.page, per_page=pagination.per_page, count=True
        )
        return (
            PaginationData(
                page=results.page, per_page=results.per_page, total=results.total
            ),
            results.items,
        )

    def query(self):
        return self.db.query(self.model)
