NORMAL_SCOPES = "profile zone user:list dns-request api-token:list api-token:create api-token:destroy refresh dns-record:list dns-record:show dns-server:list dns-server:show"
SUPER_SCOPES = (
    "profile super zone user dns-request api-token refresh dns-record dns-server"
)  # grant access to super routes

PUBLISH_SCOPES = "zone:publish dns-request:publish refresh"
