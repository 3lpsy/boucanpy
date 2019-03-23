from os.path import abspath, dirname, join

_utils_dir = abspath(dirname(__file__))

def _ajoin(target, path):
    return abspath(join(target, path))

def core_dir(path=None):
    if not path:
        return _ajoin(_utils_dir, '..')
    return _ajoin(core_dir(), path)

def project_dir(path=None):
    if not path:
        return _ajoin(core_dir(), '..')
    return _ajoin(project_dir(), path)

def cli_dir(path=None):
    if not path:
        return project_dir('cli')
    return _ajoin(cli_dir(), path)

def dns_dir(path=None):
    if not path:
        return project_dir('dns')
    return _ajoin(dns_dir(), path)

def api_dir(path=None):
    if not path:
        return project_dir('api')
    return _ajoin(api_dir(), path)
    
def web_dir(path=None):
    if not path:
        return project_dir('web')
    return _ajoin(web_dir(), path)

def root_dir(path=None):
    if not path:
        return _ajoin(project_dir(), '..')
    return _ajoin(root_dir(), path)