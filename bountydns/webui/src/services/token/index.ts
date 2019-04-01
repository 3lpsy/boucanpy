import Cookie from 'js-cookie';
import jwtDecode from 'jwt-decode';
import {Token as TokenData, TokenPayload} from '@/types';

const COOKIE_NAME = process.env.VUE_APP_COOKIE_NAME || 'auth_token';

class Token {
    cookie(): string {
        let cookie = Cookie.get(COOKIE_NAME);
        if (!cookie || typeof cookie !== 'string') {
            return '';
        }
        return cookie;
    }

    exists(): boolean {
        return this.cookie().length > 0;
    }

    save(accessToken: string) {
        return Cookie.set(COOKIE_NAME, accessToken)
    }

    remove() {
        return Cookie.remove(COOKIE_NAME)
    }

    parse(accessToken: string) : TokenData {
        let payload = (jwtDecode(accessToken) as TokenPayload);
        let scopes = payload.scopes || '';

        return {
            sub: payload.sub,
            scopes: scopes.split(' '),
            exp: payload.exp
        }
    }

    get(): string {
        return this.cookie()
    }
}

export default new Token();
