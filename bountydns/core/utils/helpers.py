def only(data, grab):
    return dict((g, data[g]) for g in grab if g in data)
