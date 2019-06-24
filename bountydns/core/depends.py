from fastapi import Depends as FADepends


def Depends(*args, **kwargs):
    return FADepends(*args, **kwargs)

