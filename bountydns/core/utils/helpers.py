from fastapi import HTTPException
from os import environ


def only_values(l, grab):
    return [v for v in l if v in grab]


def only(data, grab, values=False):
    if not grab:
        grab = []
    if not data:
        data = {}
    if values:
        return only_values(data, grab)
    if not isinstance(data, dict):
        data = dict(data)
    return dict((g, data[g]) for g in grab if g in data)


def abort(code=500, msg="Error", debug=""):
    if debug and environ.get("API_ENV", "").lower() in ["test", "local", "dev"]:
        msg = msg + "(Debug: " + str(debug) + ")"
    raise HTTPException(code, detail=msg)


def abort_for_input(field="", msg="Error", code=422, debug=""):
    if debug and environ.get("API_ENV", "").lower() in ["test", "local", "dev"]:
        msg = msg + "(Debug: " + str(debug) + ")"
    detail = [{"loc": ["body", "form", field], "msg": msg, "type": "value_error"}]
    raise HTTPException(code, detail=detail)
