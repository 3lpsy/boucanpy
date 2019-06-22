import Cookie from 'js-cookie';
import jwtDecode from 'jwt-decode';
import { Token as TokenData, TokenPayload } from '@/types';

const COOKIE_NAME = process.env.VUE_APP_COOKIE_NAME || 'auth_token';
const WS_COOKIE_NAME = process.env.VUE_APP_WS_COOKIE_NAME || 'ws_auth_token';

class Token {
    cookie(): string {
        let cookie = Cookie.get(COOKIE_NAME);
        if (!cookie || typeof cookie !== 'string') {
            return '';
        }
        return cookie;
    }

    cookieWS(): string {
        let cookie = Cookie.get(WS_COOKIE_NAME);
        if (!cookie || typeof cookie !== 'string') {
            return '';
        }
        return cookie;
    }

    exists(): boolean {
        return this.cookie().length > 0;
    }

    save(accessToken: string) {
        console.log(`Saving cookie ${COOKIE_NAME}: ${accessToken}`);
        return Cookie.set(COOKIE_NAME, accessToken);
    }

    saveWS(wsAccessToken: string) {
        console.log(`Saving cookie ${WS_COOKIE_NAME}: ${wsAccessToken}`);
        return Cookie.set(WS_COOKIE_NAME, wsAccessToken);
    }

    remove() {
        return Cookie.remove(COOKIE_NAME);
    }

    parse(accessToken: string): TokenData {
        let payload = jwtDecode(accessToken) as TokenPayload;
        let exp = payload.exp;
        let scopes = payload.scopes || '';

        return {
            sub: payload.sub,
            scopes: scopes.split(' '),
            exp: exp,
            token: accessToken,
        };
    }

    get(): string {
        return this.cookie();
    }

    getWS(): string {
        return this.cookieWS();
    }
}

export default new Token();
