from jinja2 import Environment, FileSystemLoader, select_autoescape
from bountydns.core.utils import webui_dir

loader = FileSystemLoader(webui_dir("dist"))

jinja2 = Environment(loader=loader, autoescape=False)
