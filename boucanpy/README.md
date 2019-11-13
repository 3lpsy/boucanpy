# Primary Code

This directory contains the primary code for the API and DNS Server. The api server is started via boucanpy/cli/api/api_server.py and the dns server is started via boucanpy/cli/dns/dns_server.py.

## Folders

### API

The API directory contains the FastAPI application instance, the API config, and the Controller methods (routers).

### Broadcast

The broadcast directory contains the redis instance and utility methods which allow for broadcasting messages over websockets to work.

### Core

The core directory contains many different components that are used in both the API and DNS servers. Primarily, it contains different "entity" classes. Entity classes could refer to a response class, a data class, a form class, or repo class related to a data model (the model class is not in this directory). This directory also contains security utilities as well as general utilities/helpers.

As part of the entity classes, a repo class is a helper class that allows for easily building database queries for a model as well as transforming the results to a data class.

### DB

The DB directory contains database models, migrations, factories, queries, and db instances (utility methods).

### DNS

The DNS directory contains DNS specifiy logic such as an api_client the dns server can use to talk back to the API server and other useful classes like resolvers and loggers.

### Storage

Files related to either the API or DNS should be saved here. No python logic lives in this directory
