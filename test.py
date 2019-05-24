import yaml
import re
import os

path_matcher = re.compile(r".*\$\{([^}^{]+)\}.*")


def path_constructor(loader, node):
    return os.path.expandvars(node.value)


class EnvVarLoader(yaml.SafeLoader):
    pass


EnvVarLoader.add_implicit_resolver("!path", path_matcher, None)
EnvVarLoader.add_constructor("!path", path_constructor)

data = """
env: ${HOME}/file.txt
other: file.txt
"""

if __name__ == "__main__":
    p = yaml.load(data, Loader=EnvVarLoader)
    print(os.environ.get("HOME"))  ## /home/abc
    print(p["env"])  ## /home/abc/file.txt
