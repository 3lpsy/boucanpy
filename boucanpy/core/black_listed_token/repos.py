from boucanpy.core.base.repos import BaseRepo
from boucanpy.db.models.black_listed_token import BlackListedToken
from boucanpy.core.black_listed_token.data import BlackListedTokenData


class BlackListedTokenRepo(BaseRepo):
    default_model = BlackListedToken
    default_data_model = BlackListedTokenData
