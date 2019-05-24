from fastapi import Depends
from sqlalchemy.orm import Session
from bountydns.db.session import session
from bountydns.core.base.repos import BaseRepo
from bountydns.db.models.api_token import ApiToken
from bountydns.core.api_token.data import ApiTokenData, SensitiveApiTokenData
from bountydns.core.black_listed_token.repos import BlackListedTokenRepo


class ApiTokenRepo(BaseRepo):
    default_model = ApiToken
    default_data_model = ApiTokenData

    def __init__(
        self,
        bl_token_repo: BlackListedTokenRepo = Depends(BlackListedTokenRepo),
        db: Session = Depends(session),
    ):
        self.bl_token_repo = bl_token_repo
        super().__init__(db)

    def deactivate(self, id):
        token = super().deactivate(id).set_data_model(SensitiveApiTokenData).data()
        self.bl_token_repo.create({"token": token.token})
        return self
