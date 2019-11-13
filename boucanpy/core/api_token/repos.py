from fastapi import Depends
from sqlalchemy.orm import Session
from boucanpy.db.session import async_session
from boucanpy.core.base.repos import BaseRepo
from boucanpy.db.models.api_token import ApiToken
from boucanpy.core.api_token.data import ApiTokenData, SensitiveApiTokenData
from boucanpy.core.black_listed_token.repos import BlackListedTokenRepo


class ApiTokenRepo(BaseRepo):
    default_model = ApiToken
    default_data_model = ApiTokenData

    def __init__(self, db=None, bl_token_repo=None, **kwargs):
        self.bl_token_repo = bl_token_repo
        super().__init__(db)

    def deactivate(self, id):
        token = super().deactivate(id).set_data_model(SensitiveApiTokenData).data()
        self.bl_token_repo.create({"token": token.token})
        return self

    async def __call__(
        self,
        bl_token_repo: BlackListedTokenRepo = Depends(BlackListedTokenRepo()),
        db: Session = Depends(async_session),
    ):
        return self.new(db=db, bl_token_repo=bl_token_repo)
