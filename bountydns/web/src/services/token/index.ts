import Cookie from 'js-cookie';

const COOKIE_NAME = process.env.COOKIE_NAME || 'auth_token';

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
}

export default new Token();
