import re
from ipaddress import IPv4Address

DOMAIN_RE = re.compile("^([a-zA-Z0-9][-a-zA-Z0-9]*[a-zA-Z0-9]\.)+([a-zA-Z0-9]{2,5})$")
HOSTNAME_RE = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)


def is_valid_domain(domain):
    return DOMAIN_RE.fullmatch(domain)


def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]  # strip exactly one dot from the right, if present
    return all(HOSTNAME_RE.match(x) for x in hostname.split("."))


def is_valid_ipv4address(ip):
    try:
        ip_obj = IPv4Address(ip)
        return ip_obj
    except ValueError as e:
        return False
