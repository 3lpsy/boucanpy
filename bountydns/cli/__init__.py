from .parser import make_parser
from os import walk
from pathlib import Path
from os.path import join, basename
from importlib import import_module
from bountydns.core.utils import cli_dir, snake_to_title

commands = []


def extact_commands(parent_dir, parent_mod):
    _commands = []
    for directory_name, sub_directories, files in walk(parent_dir):
        # import each file in parent_dir
        if not basename(directory_name).startswith(("__", "base")):
            for f in sorted(files):
                if (
                    not f.startswith(("__", "base"))
                    and Path(join(parent_dir, f)).is_file()
                ):
                    base_name = f.split(".")[0]
                    class_name = snake_to_title(base_name)
                    module_path = f"{parent_mod}.{base_name}"
                    module = import_module(module_path, class_name)
                    _command = getattr(module, class_name, None)
                    if _command:
                        _commands.append(_command)
                    else:
                        print(f"failed to find command in {module_path}")

    for directory_name, sub_directories, files in walk(parent_dir):
        # loop over each sub directory in parent_dir and import those files
        for sub_dir_name in sub_directories:
            if not sub_dir_name.startswith(("__", "base")):
                sub_dir = join(parent_dir, sub_dir_name)
                _commands = _commands + extact_commands(
                    sub_dir, f"{parent_mod}.{sub_dir_name}"
                )
    return _commands


for c in extact_commands(cli_dir(), "bountydns.cli"):
    commands.append(c)
