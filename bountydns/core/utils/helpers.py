from fastapi import HTTPException


def only(data, grab):
    if not isinstance(data, dict):
        data = dict(data)
    return dict((g, data[g]) for g in grab if g in data)


def abort(code=500, msg="Error"):
    raise HTTPException(code, detail=msg)
