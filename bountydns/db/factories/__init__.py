from os import walk
from os.path import join
from importlib import import_module
from bountydns.core.utils import db_dir, snake_to_title

factories = {}

factories_dir = db_dir("factories")
for directory_name, sub_directories, files in walk(factories_dir):
    for f in sorted(files):
        if not f.startswith("__") and not f.startswith("base"):
            base_name = f.split(".")[0]
            class_name = snake_to_title(base_name) + "Factory"
            module_path = f"bountydns.db.factories.{base_name}"
            module = import_module(module_path, class_name)
            model = getattr(module, class_name)
            if class_name not in factories.keys():
                factories[class_name] = model

# aliases = [{f.alias: f} for f in factories if f.alias]


def factory(key, session=None):
    # if key in aliases:
    #     return aliases[key]
    f = factories[key]
    if session:
        f._meta.sqlalchemy_session = session
    return f
