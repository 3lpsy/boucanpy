import axios from 'axios';
import { AxiosRequestConfig } from 'axios';
import { store } from '@/store';
import { TokenPayload } from '@/types';
import router from '@/router';

import moment from 'moment';
import qs from 'qs';

import { API_URL } from '@/config';

export const makeHttp = () => {
    return axios.create({
        baseURL: API_URL,
        paramsSerializer: function(params) {
            return qs.stringify(params, {
                indices: false,
                arrayFormat: 'repeat',
            });
        },
    });
};

export const http = makeHttp();

let refreshRegistration = -1;

function isTokenExpired(token: TokenPayload): boolean {
    let expUtc = token.exp;
    let nowUtc = moment.utc().unix();
    return expUtc < nowUtc;
}

function isTokenRefreshable(token: TokenPayload): boolean {
    let expUtc = token.exp;
    let nowUtc = moment.utc().unix();
    let diff = expUtc - nowUtc;
    // expires in 5 minutes
    return diff < 300;
}

// TODO: pull from cookie instead of store?
function refreshToken(config: AxiosRequestConfig): any {
    if (store.getters['auth/hasToken']) {
        let token = store.getters['auth/getToken'];
        if (isTokenExpired(token)) {
            console.log('axios interception: deauthenticating');

            return store.dispatch('auth/deauthenticate').then(() => {
                router.push({ name: 'login' });
                return config;
            });
        } else {
            if (isTokenRefreshable(token)) {
                console.log(
                    'axios interception: triggering refresh action for token',
                );
                return store.dispatch('auth/refresh', token.token).then(() => {
                    return config;
                });
            } else {
                return config;
            }
        }
    } else {
        return config;
    }
}

// TODO: pull from cookie instead of store?
function refreshWebSocketToken(config: AxiosRequestConfig): any {
    if (store.getters['auth/hasWSToken']) {
        let wsToken = store.getters['auth/getWSToken'];
        if (isTokenExpired(wsToken)) {
            console.log('axios interception: deauthenticating');
            return store.dispatch('auth/deauthenticate').then(() => {
                router.push({ name: 'login' });
                return config;
            });
        } else {
            if (isTokenRefreshable(wsToken)) {
                console.log(
                    'axios interception: triggering action for ws token',
                );
                return store
                    .dispatch('auth/refreshWS', wsToken.token)
                    .then(() => {
                        return config;
                    });
            } else {
                return config;
            }
        }
    } else {
        return config;
    }
}

function handleError(error: any) {
    return Promise.reject(error);
}

http.interceptors.request.use(refreshToken, handleError);
http.interceptors.request.use(refreshWebSocketToken, handleError);

export function setServiceToken(jwt: string) {
    http.defaults.headers.common['Authorization'] = `Bearer ${jwt}`;
}

export function clearServiceToken() {
    delete http.defaults.headers.common['Authorization'];
}
