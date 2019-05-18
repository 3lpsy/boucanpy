def only(data, grab):
    if not isinstance(data, dict):
        data = dict(data)
    return dict((g, data[g]) for g in grab if g in data)
