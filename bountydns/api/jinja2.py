from jinja2 import Environment, FileSystemLoader, select_autoescape
from bountydns.core.utils import web_dir

loader = FileSystemLoader(web_dir("dist"))

jinja2 = Environment(loader=loader, autoescape=False)
