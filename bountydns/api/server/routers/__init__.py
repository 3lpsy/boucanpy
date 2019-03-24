from os import walk
from os.path import join
from importlib import import_module
from bountydns.core.utils import api_server_dir, snake_to_title

routers = []

for directory_name, sub_directories, files in walk(api_server_dir("routers")):
    for sub_dir_name in sorted(sub_directories):
        if not sub_dir_name.startswith(("__", "base")):
            sub_dir = join(api_server_dir("routers"), sub_dir_name)
            module_path = f"bountydns.api.server.routers.{sub_dir_name}.router"
            module = import_module(module_path, "router")
            _router = getattr(module, "router")
            _options = getattr(module, "options", {})
            router = (_router, _options)
            routers.append(router)
