from os import walk
from importlib import import_module
from bountydns.core.utils import cli_dir, snake_to_title

commands = []

for directory_name, sub_directories, files in walk(cli_dir("commands")):
    for f in sorted(files):
        if not f.startswith("__") and not f.startswith("base"):
            base_name = f.split(".")[0]
            class_name = snake_to_title(base_name)
            module_path = f"bountydns.cli.commands.{base_name}"
            module = import_module(module_path, class_name)
            command = getattr(module, class_name)
            if command not in commands:
                commands.append(command)
