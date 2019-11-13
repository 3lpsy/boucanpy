import os
from base64 import b64encode
from boucanpy.core.utils import getenv_bool, getenv
from boucanpy.db.session import db_url

API_V1_STR = "/api/v1"


API_SECRET_KEY = getenv("API_SECRET_KEY")
JWT_ALGORITHM = "HS256"

if not API_SECRET_KEY:
    API_SECRET_KEY = b64encode(os.urandom(32)).decode("utf-8")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

API_CORS_ORIGINS = getenv(
    "API_CORS_ORIGINS"
)  # a string of origins separated by commas, e.g: "http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8080, http://local.dockertoolbox.tiangolo.com"
API_PROJECT_NAME = getenv("API_PROJECT_NAME", "Bounty DNS")
SQLALCHEMY_DATABASE_URI = db_url()

API_SUPERUSER_EMAIL = getenv("API_SUPERUSER_EMAIL", optional=True)
API_SUPERUSER_PASSWORD = getenv("API_SUPERUSER_PASSWORD", optional=True)
API_SUPERUSER_MFA_SECRET = getenv("API_SUPERUSER_MFA_SECRET", optional=True)
