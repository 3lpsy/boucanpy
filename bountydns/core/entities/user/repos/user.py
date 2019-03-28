from typing import Optional, List
from bountydns.core.entities.base.repos import BaseRepo
from bountydns.db.models.user import User


class UserRepo(BaseRepo):
    model = User

    def get_by_sub(self, sub) -> Optional[User]:
        filter = {self.model.sub_field: sub}
        return self.db.query(User).filter_by(**filter).first()
