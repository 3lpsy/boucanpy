from bountydns.core import load_env

load_env("api.test")

from bountydns.api.api import api
from starlette.testclient import TestClient

client = TestClient(api)
