from sqlalchemy.event import listen
import asyncio
from bountydns.core import logger

ORM_EVENTS = ["after_insert"]


# TODO: is this a legit async approach?
def make_event(func):
    def _event(*args, **kwargs):
        loop = asyncio.get_event_loop()
        # task = loop.create_task(func(*args, **kwargs))
        logger.info(f"triggering event for function {str(func)}")
        result = asyncio.ensure_future(func(*args, **kwargs), loop=loop)
        return result

    return _event


def db_register_model_events(models):
    for m in models:
        for event_name in ORM_EVENTS:
            event_cb = "on_" + event_name
            if hasattr(m, event_cb):
                listen(m, event_name, make_event(getattr(m, event_cb)))


def db_register_search_events(session, mixin):
    listen(session, "before_commit", mixin.before_commit)
    listen(session, "before_commit", mixin.after_commit)
