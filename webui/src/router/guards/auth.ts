import { Route } from 'vue-router';
import Guard from '@/router/guards/guard';
import token from '@/services/token';
import { store } from '@/store';
import { User } from '@/types';
import bus from '@/bus';

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
        if (!store.getters['auth/hasToken'] || !store.getters['auth/hasUser']) {
            store
                .dispatch('auth/setUpAccessToken', token.cookie())
                .then((user: User) => {
                    if (!store.getters['auth/hasWSToken']) {
                        if (token.cookieWS()) {
                            store
                                .dispatch(
                                    'auth/setUpWSAccessToken',
                                    token.cookieWS(),
                                )
                                .then((token) => {
                                    next();
                                })
                                .catch((err) => {
                                    console.log(
                                        'Error during middleware authentication for setUpWsAccessToken',
                                    );
                                    console.log(err);
                                    next({ name: 'login' });
                                    throw err;
                                });
                        } else {
                            // no ws token to load, probably disabled
                            next();
                        }
                    } else {
                        next();
                    }
                })
                .catch((err) => {
                    console.log(
                        'Error during middleware authentication for setUpAccessToken',
                    );
                    console.log(err);
                    next({ name: 'login' });
                    throw err;
                });
        } else {
            next();
        }
    }
}

export class IsSuperuser extends Guard {
    protect(to: Route, from: Route, next: any): void {
        console.log('Running Guard', this);

        let user = store.getters['auth/getUser'];
        if (!user.is_superuser) {
            console.log(
                'Error during middleware authentication for IsSuperuser',
            );
            bus.$emit('APP_TOAST', {
                message: 'Only Admins can access that page.',
                options: {
                    title: 'Application Message',
                    variant: 'danger',
                    toaster: 'b-toaster-bottom-right',
                },
            });
            next({ name: 'home' });
        }
        next();
    }
}
