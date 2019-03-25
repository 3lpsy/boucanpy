# Bounty DNS: A DNS Catcher

Status: Non-functional / WIP

This project is an attempt to implement a lightweight burp collaborator-esc application and consists of two main components: a DNS Server (Custom Python Implemention with dnslib) and an API.

When answering queries, the DNS server hits the API with information regarding the DNS query. The API will then serve the log of the DNS queries via a RESTful HTTP API as well as front-end (HTML/JS) web GUI.

TODO:
- [x] Build DNS Implementation
- [x] Build CLI Foundation
- [x] Build Alembic Commands
- [ ] Build API Auth Routes
- [ ] Build API Authentication Controls
- [ ] Build API Token Capabilities (Extended Auth Tokens)
- [ ] Build API Zone / DNS Routes
- [ ] Integrate API Callbacks into DNS Server
- [ ] Build Web GUI
- [ ] Build ability for webhook's / events

```
usage: bdnsctl.py [-h]
                  {test,tests,alembic-current,alembic-downgrade,alembic-history,alembic-init,alembic-migrate,alembic-show,alembic-stamp,alembic-upgrade,zone-create,zone,zone-list,zones,api-server,api,api-urls,urls,api-zone-list,api-zones,dns-server,dns}
                  ...

positional arguments:
  {test,tests,alembic-current,alembic-downgrade,alembic-history,alembic-init,alembic-migrate,alembic-show,alembic-stamp,alembic-upgrade,zone-create,zone,zone-list,zones,api-server,api,api-urls,urls,api-zone-list,api-zones,dns-server,dns}
                        command
    test (tests)        run tests
    alembic-current     run alembic current
    alembic-downgrade   run alembic downgrade
    alembic-history     run alembic history
    alembic-init        run alembic init
    alembic-migrate     run alembic migrate
    alembic-show        run alembic show
    alembic-stamp       run alembic stamp
    alembic-upgrade     run alembic upgrade
    zone-create (zone)  create zones
    zone-list (zones)   list zones
    api-server (api)    run api server
    api-urls (urls)     list api urls
    api-zone-list (api-zones)
                        list zones via API
    dns-server (dns)    run dns server

optional arguments:
  -h, --help            show this help message and exit

 ```
