export interface LoginForm {
    username: string;
    password: string;
}

export interface Message {
    type: string;
    text: string;
}

export interface Profile {
    username: string;
    bio?: string;
    image?: string;
    following: boolean;
}

export interface User {
    id: number;
    email: string;
}

export interface ApiToken {
    id: number
    token?: string | null
    scopes: string
    is_active: boolean
}

export interface ApiTokenResponse {
    api_token: ApiToken;
    messages?: Message[]
    pagination?: object
}

export interface ApiTokensResponse {
    api_tokens: ApiToken[];
    messages?: Message[]
    pagination?: object
}

export interface ApiTokenCreateForm {
    scopes: string
    expires_at: number
}

export interface DnsRequest {
    id: number
    name: string
    zone_id: number | null
    source_address: string
    source_port: number
    type: string
    protocol: string
}

export interface DnsRequestsResponse {
    dns_requests: DnsRequest;
    messages?: Message[]
    pagination?: object
}

export interface UserResponse {
    user: User;
    messages?: Message[]
    pagination?: object
}
export interface TokenPayload {
    sub: string;
    exp: string;
    scopes: string;
}

export interface Token {
    sub: string;
    exp: string;
    scopes: string[];
}

export interface UserForUpdate {
    email?: string;
    username?: string;
    bio?: string;
    password?: string;
    image?: string;
}

export interface Article {
    slug: string;
    title: string;
    description: string;
    body: string;
    tagList?: (string)[] | null;
    createdAt: string;
    updatedAt: string;
    favorited: boolean;
    favoritesCount: number;
    author: Author;
}
export interface Author {
    username: string;
    bio: string;
    image: string;
    following: boolean;
}

export interface UserSubmit {
    email: string;
    password: string;
}

export interface UserResponse {
    user: User;
}

export interface ProfileResponse {
    profile: Profile;
}

export interface ArticlesResponse {
    articles?: (Article)[] | null;
    articlesCount: number;
}
