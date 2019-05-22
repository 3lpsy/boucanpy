from fastapi import HTTPException


def only_values(l, grab):
    return [v for v in l if v in grab]


def only(data, grab, values=False):
    if values:
        return only_values(data, grab)
    if not isinstance(data, dict):
        data = dict(data)
    return dict((g, data[g]) for g in grab if g in data)


def abort(code=500, msg="Error"):
    raise HTTPException(code, detail=msg)
