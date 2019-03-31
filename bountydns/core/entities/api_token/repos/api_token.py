from bountydns.core.entities.base.repos import BaseRepo
from bountydns.db.models.api_token import ApiToken
from bountydns.core.entities.api_token.data import ApiTokenData


class ApiTokenRepo(BaseRepo):
    default_model = ApiToken
    default_data_model = ApiTokenData
