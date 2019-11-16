# Boucan: A Bug Bounty Canary Platform

![Screenshot](screenshots/diagram.png)

This project is an attempt to implement a lightweight burp collaborator-esc application and consists of two main components: a DNS Server (Custom Python Implemention with dnslib) and an API. It is still very much in the early days of development. You can think of Boucan as sort of a Canary that will notify you when an external asset (DNS Record, HTTP Server, SMTP Server) has been interacted with. This is useful for blind payload injection.

For more information on Burp Collaborator, checkout [burp's documentation](https://portswigger.net/burp/documentation/collaborator)

When answering queries, the DNS server hits the API with information regarding the DNS query. The API will then serve the log of the DNS queries via a RESTful HTTP API as well as front-end (HTML/JS) web GUI.

### Getting Started Quickly

The docker-compose project exists here: [Boucan Compose](https://github.com/3lpsy/boucan-compose)

```
## make a directory to hold all projects
$ mkdir boucan;
## move to that directory
$ cd boucan;
## clone the compose project
$ git clone git@github.com:3lpsy/boucan-compose.git
## cd into the compose directory
$ cd boucan-compose;
## run the setup script from inside the compose directory
$ ./setup.sh
```

Below are the steps for getting the developer server up and running. You'll obviously want to not do this for prod.

Next, you'll need to set two envrionment variables using the same secret as the API server. For the dev server, the secret is "helloworld". You can use the super tiny jwt.py script to generate these secrets assuming you have python-jwt installed.

```
## inside the compose directory
$ ./makejwt.py -S helloworld -n mynode
## afterwards, set HTTP_API_TOKEN and DNS_API_TOKEN to the value of the output (excluding "TOKEN:" prefix)

## alternatively, you can do this fun stuff and it'll automatically update the environment
$ source <(./makejwt.py -S helloworld -n mynode --exportformat)

## finally, you can also just place the the export commands in compose.env if want so they always import. it's up to you
$ ./makejwt.py -S helloworld -n mynode --exportformat >> compose.env
```

Once all the projects have been cloned and the HTTP_API_TOKEN and DNS_API_TOKEN are set, you can start the server by using the compose.sh script. Below is how to start the dev server:

```
## inside the compose directory
$ ./compose.sh dev build
$ ./compose.sh dev up
```

## Deploying

A terraform + packer project exists here: [Boucan Deploy](https://github.com/3lpsy/boucan-deploy)

## Automating

A Burp Extension which automates some injection can be found here: [Boucan Burp Extension](https://github.com/3lpsy/boucan-burpex)

## Developing

The "dev" version of the docker-compose project syncs volumes to the container and so the api will automatically reload. It also syncs the "dist" folder (for the boucan-web project). However, to have the changes reflected in the container without restarting it, you can follow the following steps

### Build the Frontend application

This is only required for development containers where the front end code is mounted.

```
## from the root boucan directory
$ cd boucan-web
$ npm install
$ npm run build

# alternatively, you can run watch to automatically rebuild the frontend

$ npm run watch
```

### Running the Services

Run the following to run the containers.

```
$ ./compose.sh dev up
```

### Restarting the Services

```
$ ./compose.sh dev fresh
```

## What does it do?

It doesn't do much really. The project will set up an API, a web interface, and a DNS server. When the DNS server receives a DNS request, it will tell the API. The API will then tell the web interface.

![Screenshot](screenshots/screenshot-dns-requests.png)

You can also see the raw request:

![Screenshot](screenshots/screenshot-dns-request.png)

This information is useful for testing the injection of domains into payloads in attacks such as Blind Cross Site scripting, Remote File Inclusion, Blind SQL Injection, Blind XML External Entity Injection, and Server Side Request Forgery.

And that's basically it. A Burp Extension is in the works in the spirit of Collaborator Everywhere which will (hopefully) be used to inject targeted zones into web requests and poll the API for updates (like Collaborator). You can currently manage these "zones" within the web interface.

![Screenshot](screenshots/screenshot-zones.png)

In addition, there's an Packer build and Terraform deployment in the "infra" folder for easy deploying.

## About the Project

The following details the general outline for the future of this project.

## Phase 1: Build the PoC

The first iteration of the project will be a proof of concept to demonstrate the project's viability. At this point, the project should not be considered stable, secure, or feature complete.

Features:

- Create API Tokens via WebUI / CLI for Dns Servers
- Create Zones for Specific DNS Servers
- Log DNS Resolution

## Phase 2: Polish The Code

After demonstrating that the project is worth dedicating time to, Phase 2 will involve making the project feature complete with all clients (WebUI / CLI) and features (webhooks / email / queue) com name, path, source_address, source_port, type, protocol, raw_request,

- Manage DNS Records through WebUI / API
- Ability to update the DNS server's records for running DNS Server (Polling)
- Receive Notifications on DNS Resolution via email or webhook
- Easily build the application with Docker, Packer, & Terraform

## Phase 3: Stability (Current)

Next, sanity checks and proper handlers will be put in place so that API calls fail gracefully. At this point the project should not be considered secure.

Features:

- Actual validation & Error Handling

## Phase 4: Release 0.1.0-alpha

Once I'm satisfied the code is not complete trash, I'll release it as version 0.1.0-alpha. At this point, the project should be considered secure enough to deploy. Though I'd recommend doing so in a protected network. If the application proves valuable enough to me personally or others, I'll continue to add features / improvements.

## Phase 5: Extending the Application

Once the core DNS use case is satisfied, the API will be extended to support the resolution of HTTP/S and SMTP requests.

TODO:

- [ ] Add SSL capabilities to http node
- [ ] Fix packer/terraform to incorporate http/s node
- [ ] Fix scope requirement bypass via includes
- [ ] Reorg project into multiple projects (api, dns, http, common, webui, deploy, compose, burp)

### Contributing

If you're interested in contributing or collaborating, you can reach out to me on twitter @3lpsy or open a github issue.

```
usage: bdnsctl.py [-h]
                  {db-seed,seed,db-setup,setup,db-truncate,truncate,test,tests,api-token-create,api-token,api-token-list,api-tokens,dns-server,dns,user-create,user,user-list,users,api-login,login,api-server,api,api-urls,urls,api-user-create,api-user,api-user-list,api-users,api-zone-create,api-zone,api-zone-list,api-zones,zone-create,zone,zone-list,zones,alembic-current,al-current,alembic-downgrade,al-downgrade,alembic-history,al-history,alembic-init,al-init,alembic-migrate,al-migrate,alembic-show,al-show,alembic-stamp,al-stamp,alembic-upgrade,al-upgrade}
                  ...

positional arguments:
  {db-seed,seed,db-setup,setup,db-truncate,truncate,test,tests,api-token-create,api-token,api-token-list,api-tokens,dns-server,dns,user-create,user,user-list,users,api-login,login,api-server,api,api-urls,urls,api-user-create,api-user,api-user-list,api-users,api-zone-create,api-zone,api-zone-list,api-zones,zone-create,zone,zone-list,zones,alembic-current,al-current,alembic-downgrade,al-downgrade,alembic-history,al-history,alembic-init,al-init,alembic-migrate,al-migrate,alembic-show,al-show,alembic-stamp,al-stamp,alembic-upgrade,al-upgrade}
                        command
    db-seed (seed)      seed db
    db-setup (setup)    setup db
    db-truncate (truncate)
                        truncate db
    test (tests)        run tests
    api-token-create (api-token)
                        create api-tokens directly
    api-token-list (api-tokens)
                        list api-tokens via DB
    dns-server (dns)    run dns server
    user-create (user)  create users via DB
    user-list (users)   list users via DB
    api-login (login)   login via API
    api-server (api)    run api server
    api-urls (urls)     list api urls
    api-user-create (api-user)
                        create user via API
    api-user-list (api-users)
                        list users via API
    api-zone-create (api-zone)
                        create user via API
    api-zone-list (api-zones)
                        list zones via API
    zone-create (zone)  create zones via DB
    zone-list (zones)   list zones via DB
    alembic-current (al-current)
                        run alembic current
    alembic-downgrade (al-downgrade)
                        run alembic downgrade
    alembic-history (al-history)
                        run alembic history
    alembic-init (al-init)
                        run alembic init
    alembic-migrate (al-migrate)
                        run alembic migrate
    alembic-show (al-show)
                        run alembic show
    alembic-stamp (al-stamp)
                        run alembic stamp
    alembic-upgrade (al-upgrade)
                        run alembic upgrade
    user-create (user)  create users via DB
    user-list (users)   list users via DB
    alembic-current (al-current)
                        run alembic current
    alembic-downgrade (al-downgrade)
                        run alembic downgrade
    alembic-history (al-history)
                        run alembic history
    alembic-init (al-init)
                        run alembic init
    alembic-migrate (al-migrate)
                        run alembic migrate
    alembic-show (al-show)
                        run alembic show
    alembic-stamp (al-stamp)
                        run alembic stamp
    alembic-upgrade (al-upgrade)
                        run alembic upgrade
    zone-create (zone)  create zones via DB
    zone-list (zones)   list zones via DB
    api-login (login)   login via API
    api-server (api)    run api server
    api-urls (urls)     list api urls
    api-user-create (api-user)
                        create user via API
    api-user-list (api-users)
                        list users via API
    api-zone-create (api-zone)
                        create user via API
    api-zone-list (api-zones)
                        list zones via API
    api-token-create (api-token)
                        create api-tokens directly
    api-token-list (api-tokens)
                        list api-tokens via DB
    dns-server (dns)    run dns server

optional arguments:
  -h, --help            show this help message and exit
```
