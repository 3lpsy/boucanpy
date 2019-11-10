NORMAL_SCOPES = "profile zone user:list dns-request dns-record:list dns-record:show dns-server:list dns-server:show http-request http-server:list http-server:show api-token:list api-token:create api-token:destroy refresh"
SUPER_SCOPES = "profile super zone user dns-request dns-record dns-server http-request http-server api-token refresh"  # grant access to super routes
PUBLISH_SCOPES = "zone:publish dns-request:publish http-request:publish refresh"
NODE_SCOPES = "profile dns-request:create dns-request:list http-request:create http-request:list zone:list zone:read refresh api-token:syncable"
