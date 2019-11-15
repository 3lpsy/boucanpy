# from boucanpy.core import load_env

# load_env("api.test")

from boucanpy.api.api import api
from starlette.testclient import TestClient

client = TestClient(api)
