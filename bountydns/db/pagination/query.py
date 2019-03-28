from fastapi import HTTPException
from sqlalchemy import orm
from bountydns.db.pagination.pagination import Pagination


class PaginationQuery(orm.Query):
    def get_or_404(self, ident):
        rv = self.get(ident)
        if rv is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return rv

    def first_or_404(self):
        rv = self.first()
        if rv is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return rv

    def paginate(
        self, page=1, per_page=20, error_out=True, max_per_page=None, count=None
    ):
        if max_per_page is not None:
            per_page = min(per_page, max_per_page)

        if page < 1:
            if error_out:
                raise HTTPException(status_code=404, detail="Item not found")
            else:
                page = 1

        if per_page < 0:
            if error_out:
                raise HTTPException(status_code=404, detail="Item not found")
            else:
                per_page = 20

        items = self.limit(per_page).offset((page - 1) * per_page).all()

        if not items and page != 1 and error_out:
            raise HTTPException(status_code=404, detail="Item not found")

        if not count:
            total = None
        elif page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = self.order_by(None).count()

        return Pagination(self, page, per_page, total, items)
