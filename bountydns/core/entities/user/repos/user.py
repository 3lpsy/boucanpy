from typing import Optional, List
from bountydns.core.entities.base.repos import BaseRepo
from bountydns.db.models.user import User
from bountydns.core.entities.user.data import UserData


class UserRepo(BaseRepo):
    default_model = User
    default_data_model = UserData

    def get_by_sub(self, sub) -> Optional[User]:
        filter = {self.model().sub_field: sub}
        return self.query().filter_by(**filter).first()
