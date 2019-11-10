export interface LoginForm {
    username: string;
    password: string;
}

export interface Message {
    type: string;
    text: string;
}

export interface ApiToken {
    id: number;
    scopes: string;
    is_active: boolean;
    dns_server_id: number;
    http_server_id: number;
    created_at: number;
}

export interface ApiTokenResponse {
    api_token: ApiToken;
    messages?: Message[];
    pagination?: object;
}

export interface ApiTokensResponse {
    api_tokens: ApiToken[];
    messages?: Message[];
    pagination?: object;
}

export interface ApiTokenCreateForm {
    scopes: string;
    expires_at: number;
    dns_server_id?: number;
    http_server_id?: number;
}

export interface SensitiveApiToken {
    id: number;
    token?: string | null;
    scopes: string;
    is_active: boolean;
    dns_server_id?: number;
    http_server_id?: number;
    created_at: number;
}

export interface SensitiveApiTokenResponse {
    api_token: SensitiveApiToken;
    messages?: Message[];
    pagination?: object;
}

export interface ZoneFormData {
    ip: string;
    domain: string;
    dns_server_id?: string;
    http_server_id?: string;
}

export interface Zone {
    id: number;
    domain: string;
    ip: string;
    is_active: boolean;
    dns_server_id?: string;
    http_server_id?: string;
    created_at: number;
}

export interface ZoneResponse {
    zone: Zone;
    messages?: Message[];
    pagination?: object;
}

export interface ZonesResponse {
    zones: Zone[];
    messages?: Message[];
    pagination?: object;
}

export interface ZoneCreateForm {
    domain: string;
    ip: string;
    dns_server_name?: string;
    http_server_name?: string;
}

export interface DnsRequest {
    id: number;
    name: string;
    zone_id: number | null;
    zone?: Zone;
    source_address: string;
    source_port: number;
    type: string;
    protocol: string;
    dns_server_id: number;
    dns_server?: DnsServer;
    created_at: number;
    raw_request: string;
}

export interface DnsRequestResponse {
    dns_request: DnsRequest;
    messages?: Message[];
    pagination?: object;
}

export interface DnsRequestsResponse {
    dns_requests: DnsRequest[];
    messages?: Message[];
    pagination?: object;
}

export interface HttpRequest {
    id: number;
    name: string;
    path: string;
    zone_id: number | null;
    zone?: Zone;
    source_address: string;
    source_port: number;
    type: string;
    protocol: string;
    http_server_id: number;
    http_server?: DnsServer;
    created_at: number;
    raw_request: string;
}

export interface HttpRequestResponse {
    http_request: HttpRequest;
    messages?: Message[];
    pagination?: object;
}

export interface HttpRequestsResponse {
    http_requests: HttpRequest[];
    messages?: Message[];
    pagination?: object;
}

export interface User {
    id: number;
    email: string;
    is_superuser?: boolean;
    is_active?: boolean;

    created_at: number;
}

export interface UserCreateForm {
    email: string;
    is_superuser?: boolean;
    password: string;
    password_confirm: string;
}

export interface UserResponse {
    user: User;
    messages?: Message[];
    pagination?: object;
}

export interface UsersResponse {
    user: User[];
    messages?: Message[];
    pagination?: object;
}

export interface TokenPayload {
    sub: string;
    exp: number;
    scopes: string;
    token: string;
}

export interface DnsServer {
    id: number;
    name: string;
    zones: Zone[];
    created_at: number;
}

export interface DnsServerCreateForm {
    name: string;
}

export interface DnsServerResponse {
    dns_server: DnsServer;
    messages?: Message[];
}

export interface DnsServersResponse {
    dns_servers: DnsServer[];
    messages?: Message[];
    pagination?: object;
}

export interface HttpServer {
    id: number;
    name: string;
    zones: Zone[];
    created_at: number;
}

export interface HttpServerCreateForm {
    name: string;
}

export interface HttpServerResponse {
    http_server: HttpServer;
    messages?: Message[];
}

export interface HttpServersResponse {
    http_servers: HttpServer[];
    messages?: Message[];
    pagination?: object;
}

export interface DnsRecordForZoneCreateForm {
    record: string;
    sort: number;
}

export interface DnsRecordCreateForm {
    record: string;
    sort: number;
    zone_id: number;
}

export interface DnsRecord {
    id: number;
    record: string;
    sort: number;
    zone_id: number;
    zone?: Zone;
}

export interface DnsRecordResponse {
    dns_record: DnsRecord;
    messages?: Message[];
}

export interface DnsRecordsDigResponse {
    dig: string;
    messages?: Message[];
    pagination?: object;
}

export interface DnsRecordsResponse {
    dns_records: DnsRecord[];
    messages?: Message[];
    pagination?: object;
}

export interface Token {
    sub: string;
    exp: number;
    scopes: string[];
    token: string;
}
