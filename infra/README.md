# Infrastucture

This directory holds the supporting Infrastucture. Primarily, it holds the Dockerfiles and Docker Compose project necessary for building the application. Eventually it hold additional configs for packer and terraform.

## Directories

### Broadcast

The broadcast directory holds files related to the broadcast (redis) instance. Files in this case will most likely be bundled into the broadcast(redis) container image.

### Compose

The compose directory contains the docker-compose files. To load these files together, use compose.sh in the root directory.

### DBUI

The dbui contains files that may be bundled into the dbui (pgadmin) container. The dbui container is meant for development, not production.

### Docker

The Dockerfiles for each container exist in this directory. For example, bountydns.dockerfile is used to build the image that is used by the DNS and API instances.

### Packer

This folder will container packer files.

### Proxy

This directory contains files needed to build to the proxy (nginx) server such as the nginx.conf file.

### Scripts

Generic scripts go here

### Terraform

This folder will contain terraform files.
