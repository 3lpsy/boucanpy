from bountydns.core.base.repos import BaseRepo
from bountydns.db.models.black_listed_token import BlackListedToken
from bountydns.core.black_listed_token.data import BlackListedTokenData


class BlackListedTokenRepo(BaseRepo):
    default_model = BlackListedToken
    default_data_model = BlackListedTokenData
