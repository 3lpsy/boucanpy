from typing import Optional, List
from fastapi import Depends
from sqlalchemy.orm import Session
from bountydns.db.session import session
from bountydns.db.pagination import Pagination
from bountydns.core.entities.pagination.responses import PaginationData


class BaseRepo:
    default_model = None
    default_data_model = None

    def __init__(self, db: Session = Depends(session)):
        self.db = db
        self._query = None
        self._results = None
        self._data_model = None
        self._model = None
        self._is_paginated = False
        self._is_list = False  # check at runtime instead (?)

    def results(self):
        return self._results

    def data(self):
        if self._is_paginated:
            return self.paginated_data()
        if self._is_list:
            return [self.data_model()(**r.as_dict()) for r in self.results()]
        return self.data_model()(**self.results().as_dict())

    def paginated_data(self):
        return (
            PaginationData(
                page=self._results.page,
                per_page=self._results.per_page,
                total=self._results.total,
            ),
            [self.data_model()(**r.as_dict()) for r in self._results.items],
        )

    def get(self, id):
        self._results = self.query().get(id)
        return self

    def all(self):
        self._results = self.query().all()
        self._is_list = True
        return self

    def paginate(self, pagination):
        self._results = self.query().paginate(
            page=pagination.page, per_page=pagination.per_page, count=True
        )
        self._is_paginated = True
        return self

    def create(self, data):
        try:
            instance = self.model()(**dict(data))
            self.db.add(instance)
            self.db.commit()
            self.db.flush()
            self._results = instance
            return self
        except Exception as e:
            self.db.rollback()
            raise e

    def query(self):
        if not self._query:
            self._query = self.db.query(self.model())
        return self._query

    def set_data_model(self, data_model):
        self._data_model = data_model
        return self

    def model(self):
        return self._model or self.default_model

    def data_model(self):
        return self._data_model or self.default_data_model
