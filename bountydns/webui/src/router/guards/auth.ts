import { Route } from 'vue-router';
import Guard from '@/router/guards/guard';
import token from '@/services/token';
import {store } from '@/store';
import { User } from '@/types';

export class HasAuthenticationCookie extends Guard {
    protect(to: Route, from: Route, next: any): void {
        console.log('Running Guard', this);
        if (!token.exists()) {
            console.log('No token found. Redirecting');
            next({ name: 'login' });
        }
        next();
    }
}

export class IsAuthenticated extends Guard {
    protect(to: Route, from: Route, next: any): void {
        console.log('Running Guard', this);
        if (! store.getters['auth/hasToken'] || ! store.getters['auth/hasUser']) {
            store.dispatch('auth/authenticateWithToken', {accessToken: token.cookie(), wsAccessToken: token.cookieWS()}).then((user: User) => {
                next()
            }).catch((err) => {
                console.log("Error during middleware authentication")
                next({ name: 'login' });
                throw err

            })
        } else {
            next();
        }
    }
}
