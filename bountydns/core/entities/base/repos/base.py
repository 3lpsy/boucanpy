from typing import Optional, List
from fastapi import Depends
from sqlalchemy.dialects import postgresql
from sqlalchemy import or_, desc
from sqlalchemy.orm import Session, joinedload
from bountydns.core import logger
from bountydns.db.session import session
from bountydns.db.pagination import Pagination
from bountydns.core.entities.pagination.responses import PaginationData


class BaseRepo:
    default_model = None
    default_data_model = None
    default_loads = []
    default_fitlers = []

    def __init__(self, db: Session = Depends(session)):
        self.db = db
        self._query = None
        self._results = None
        self._data_model = None
        self._model = None
        self._is_paginated = False
        self._is_list = False  # check at runtime instead (?)
        self._filters = {}

    ## RESULTS
    def results(self):
        return self._results

    def set_results(self, results):
        # TODO: not compatible with list / pagination / see above
        self._results = results
        return self

    def load(self, loads):
        for load in loads:
            if hasattr(self, "load_" + load):
                self._query = hasattr(self, "load_" + load)()
            else:
                self_query = self.query().options(joinedload(load))
        return self

    ## DATA
    def data(self):
        if self._is_paginated:
            return self.paginated_data()
        if self._is_list:
            return [self.to_data(r) for r in self.results()]
        return self.to_data(self.results())

    def paginated_data(self):
        return (
            PaginationData(
                page=self._results.page,
                per_page=self._results.per_page,
                total=self._results.total,
            ),
            [self.to_data(r) for r in self._results.items],
        )

    def to_data(self, item):
        if not item:
            return None
        return self.data_model()(**self.to_dict(item))

    def to_dict(self, item):
        return item.as_dict() if hasattr(item, "as_dict") else dict(item)

    ## EXECUTION
    def exists(self, id=None, **kwargs):
        if id and not kwargs:
            self.filter_by(id=id)
        elif kwargs:
            self.filter_by(**kwargs)
        self.debug(
            f"executing first (exists) query {self.compiled()} in {self.__class__.__name__}"
        )
        results = self.query().first()
        self._results = results
        return bool(self._results)

    def first(self, **kwargs):
        if kwargs:
            self.filter_by(**kwargs)
        self.debug(
            f"executing first query {self.compiled()} in {self.__class__.__name__}"
        )
        self._results = self.query().first()
        return self

    def get(self, id):
        self.debug(
            f"executing get query {self.compiled()} in {self.__class__.__name__}"
        )
        return self.query().get(id)

    def all(self, **kwargs):
        if kwargs:
            self.filter_by(**kwargs)
        self.debug(
            f"executing all query {self.compiled()} in {self.__class__.__name__}"
        )
        self._results = self.query().all()
        self._is_list = True
        return self

    def paginate(self, pagination):
        self.debug(
            f"executing page query {self.compiled()} in {self.__class__.__name__}"
        )
        self._results = self.query().paginate(
            page=pagination.page, per_page=pagination.per_page, count=True
        )
        self._is_paginated = True
        return self

    ## FILTERS / MODIFICATION

    def search(self, search_qs):
        if not search_qs:
            return self
        # TODO: implement search functionality
        return self

    def sort(self, sort_qs):
        sort = self.get_sort_by(sort_qs.sort_by)
        if sort_qs.sort_dir.lower() == "desc":
            sort = desc(sort)
        self._query = self.query().order_by(sort)
        return self

    def get_sort_by(self, key):
        return self.label(key)

    def filters(self, key, *args, **kwargs):
        if hasattr(self, "filter_" + key):
            getattr(self, "filter_" + key)(*args, **kwargs)
        elif key in self._filters:
            if callable(self._filters[key]):
                self.query = self.self._filters[key](self.query(), *args, **kwargs)
        return self

    def add_filter(self, key, filter):
        self._filters[key] = filter
        return self

    def filter_or(self, *args, **kwargs):
        self._query = self.query().filter(or_(*args, **kwargs))
        return self

    def filter_by(self, **kwargs):
        self._query = self.query().filter_by(**kwargs)
        self.debug(f"adding filters {kwargs} to query {self.compiled()}")
        return self

    def filter(self, *args, **kwargs):
        self._query = self.query().filter(*args, **kwargs)
        self.debug(f"adding filters {args} and {kwargs} to query {self.compiled()}")
        return self

    ## COMMITTING / UPDATING
    def deactivate(self, id):
        self.get(id)
        self.update({"is_active": False})
        return self

    def update(self, data):
        # TODO: make work with list
        try:
            instance = self.results()
            for attr, value in dict(data).items():
                setattr(instance, attr, value)
            self.db.add(instance)
            self.db.commit()
            self.db.flush()
            self._results = instance
            return self
        except Exception as e:
            self.db.rollback()
            raise e

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

    ## GETTERS
    def query(self):
        if not self._query:
            self.debug(f"making query for repo: {self.__class__.__name__}")
            self._query = self.db.query(self.model())
            self.load(self.default_loads)
        return self._query

    def compiled(self):
        return str(
            self.query().statement.compile(
                dialect=postgresql.base.PGDialect(),
                compile_kwargs={"literal_binds": True},
            )
        )

    def set_data_model(self, data_model):
        self._data_model = data_model
        return self

    def label(self, key):
        return getattr(self.model(), key)

    def model(self):
        return self._model or self.default_model

    def model_column(self, key):
        return getattr(self.model(), key)

    def data_model(self):
        return self._data_model or self.default_data_model

    def debug(self, msg):
        pass
        # logger.debug(msg)

    def clear(self):
        self._query = None
        self._results = None
        self._data_model = None
        self._model = None
        self._is_paginated = False
        self._is_list = False  # check at runtime instead (?)
        self._filters = {}
        return self
