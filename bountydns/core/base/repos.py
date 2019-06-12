from typing import Optional, List
from fastapi import Depends

from sqlalchemy import or_, desc, func, cast, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session, joinedload, raiseload

from bountydns.core import logger, abort
from bountydns.db.session import session
from bountydns.db.pagination import Pagination
from bountydns.core.pagination.data import PaginationData


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
        self._options = []
        self._includes = {}

    ## RESULTS
    def results(self):
        return self._results

    def set_results(self, results):
        # TODO: not compatible with list / pagination / see above
        self._results = results
        return self

    def loads(self, load):
        if not load:
            return self
        if isinstance(load, list):
            for _load in load:
                self._options.append(self._loader(_load))
        elif isinstance(load, str):
            self._options.append(self._loader(load))
        else:
            raise Exception(f"Loader failed for repo: {load}")
        return self

    def _loader(self, load):
        if isinstance(load, str):
            if hasattr(self, "load_" + load):
                return getattr(self, "load_" + load)()
            elif "." in load:
                under_load = load.replace(".", "_")
                if hasattr(self, "load_" + under_load):
                    return getattr(self, "load_" + under_load)()
                return self._loader_chain(load)
            elif load in self.model().__mapper__.relationships.keys():
                return joinedload(self.label(load))
            else:
                raise Exception(f"Loader failed for repo: {load}")
        return load

    def _loader_chain(self, load):
        chain = None
        parent = self.model()
        for part in load.split("."):
            chain = (
                chain.joinedload(getattr(parent, part))
                if chain
                else joinedload(getattr(parent, part))
            )
            parent = self._get_relationship_model(part, parent)

        return chain

    def _get_relationship_model(self, name, model=None):
        model = model or self.model()
        # TODO: add some __loadable__ attribute to base model to prevent dangerous loads
        #       or add some _loadable whitelist to each repo
        return getattr(model.__mapper__.relationships, name).mapper.class_

    def strict(self, rel="*"):
        self._options.append(raiseload(rel))
        return self

    def includes(self, prop, key=None):
        if not prop:
            return self
        if isinstance(prop, list):
            for _prop in prop:
                if isinstance(_prop, tuple):
                    self._includes[_prop[0]] = _prop[1]
                else:
                    self._includes[_prop] = _prop
        elif isinstance(prop, dict):
            for include_prop, include_key in prop.items():
                self._includes[include_prop] = include_key
        else:
            key = key or prop
            self._includes[prop] = key
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
        attrs = self.to_dict(item)
        return self.data_model()(**attrs)

    def to_dict(self, item):
        root_data = item.as_dict() if hasattr(item, "as_dict") else dict(item)
        self.debug(
            f"attaching includables {str(self._includes)} in {self.__class__.__name__}"
        )
        for name in self._includes.keys():
            if name not in root_data:
                if not hasattr(item, name):
                    self.debug(f"cannot find attr {str(name)} on item {str(item)}")
                    continue
                # TODO: what if 0
                elif not getattr(item, name):
                    prop_key = self._includes[name]
                    root_data[prop_key] = None
                else:
                    prop = getattr(item, name)
                    self.debug(f"getting attr {str(name)} on item {str(item)}")
                    # prop can be list
                    if isinstance(prop, list):
                        prop_data = []
                        for prop_item in prop:
                            # TODO: what if includabes are primitives or non-dict
                            prop_item_data = (
                                prop_item.as_dict()
                                if hasattr(prop_item, "as_dict")
                                else dict(prop_item)
                            )
                            prop_data.append(prop_item_data)
                    # prop can be dictable
                    else:
                        prop_data = (
                            prop.as_dict() if hasattr(prop, "as_dict") else dict(prop)
                        )
                    prop_key = self._includes[name]

                    # self.debug(
                    #     f"attaching attr {str(name)} on item {str(item)} with data {str(prop_data)}"
                    # )

                    root_data[prop_key] = prop_data
        return root_data

    ## EXECUTION
    def exists(self, id=None, or_fail=False, **kwargs):
        if id and not kwargs:
            self.filter_by(id=id)
        elif kwargs:
            self.filter_by(**kwargs)
        self.debug(
            f"executing first (exists) query {self.compiled()} in {self.__class__.__name__}"
        )
        results = self.final().first()
        if or_fail and not results:
            abort(404, f"Item not found: {self.__class__.__name__}")
        self._results = results
        return bool(self._results)

    def exists_or_fail(self, **kwargs):
        return self.exists(or_fail=True, **kwargs)

    def first(self, or_fail=False, **kwargs):
        if kwargs:
            self.filter_by(**kwargs)
        self.debug(
            f"executing first query {self.compiled()} in {self.__class__.__name__}"
        )
        results = self.final().first()
        if or_fail:
            if not results:
                abort(404, f"Item not found: {self.__class__.__name__}")
        self._results = results
        return self

    def first_or_fail(self, **kwargs):
        return self.first(or_fail=True, **kwargs)

    def get(self, id, or_fail=False):
        return self.first(id=id, or_fail=or_fail)

    def get_or_fail(self, id):
        return self.get(id, or_fail=True)

    def all(self, **kwargs):
        if kwargs:
            self.filter_by(**kwargs)
        self.debug(
            f"executing all query {self.compiled()} in {self.__class__.__name__}"
        )

        self._results = self.final().all()
        self._is_list = True
        return self

    def paginate(self, pagination):
        self.debug(
            f"executing page query {self.compiled()} in {self.__class__.__name__}"
        )
        self._results = self.final().paginate(
            page=pagination.page, per_page=pagination.per_page, count=True
        )
        self._is_paginated = True
        return self

    ## FILTERS / MODIFICATION

    def search(self, search, searchable=None):
        if not search:
            return self

        if not searchable:
            searchable = self.model().__searchable__

        if not searchable:
            raise Exception(f"No search models found for query: {search_qs}")

        # TODO: implement search functionality in elasticsearch
        clauses = []
        for col in searchable:
            if col == "id" or col.endswith((".id", "_id")):
                label = cast(self.label(col), String)
            else:
                label = func.lower(self.label(col))
            clauses.append(label.contains(search))

        self.filter_or(*clauses)

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
        return self

    def filter_or(self, *args, **kwargs):
        self._query = self.query().filter(or_(*args, **kwargs))
        return self

    def filter_by(self, **kwargs):
        self._query = self.query().filter_by(**kwargs)
        # self.debug(f"adding filters {kwargs} to query {self.compiled()}")
        return self

    def filter(self, *args, **kwargs):
        self._query = self.query().filter(*args, **kwargs)
        # self.debug(f"adding filters {args} and {kwargs} to query {self.compiled()}")
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
            if not isinstance(data, dict):
                data = dict(data)
            for attr, value in data.items():
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
            if not isinstance(data, dict):
                data = dict(data)
            instance = self.model()(**data)
            self.db.add(instance)
            self.db.commit()
            self.db.flush()
            self._results = instance
            return self
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self):
        try:
            instance = self.results()
            self.db.delete(instance)
            self.db.commit()
            self.db.flush()
            self._results = instance
            return self
        except Exception as e:
            self.db.rollback()
            raise e

    ## GETTERS

    def final(self, attach=True):
        self._query = self.query().options(*self._options)
        return self.query()

    def query(self):
        if not self._query:
            # self.debug(f"making query for repo: {self.__class__.__name__}")
            self._query = self.db.query(self.model())
            self.loads(self.default_loads)
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
        if "." not in key:
            return getattr(self.model(), key)
        parent = self.model()
        parts = key.split(".")
        final_index = len(parts) - 1
        for i, part in enumerate(parts):
            if i == final_index:
                logger.critical("LABEL " + str(getattr(parent, part)))
                return getattr(parent, part)
            parent = self._get_relationship_model(part, parent)
        raise Exception(f"Unable to decipher label for key: {key}")

    def model(self):
        return self._model or self.default_model

    def data_model(self):
        return self._data_model or self.default_data_model

    def debug(self, msg):
        # pass
        logger.info(msg)

    def clear(self):
        self._query = None
        self._results = None
        self._data_model = None
        self._model = None
        self._is_paginated = False
        self._is_list = False  # check at runtime instead (?)
        self._options = []
        self._includes = {}
        return self
