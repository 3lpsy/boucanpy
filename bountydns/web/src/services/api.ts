import axios from 'axios';
import {AxiosRequestConfig } from 'axios';
import {store} from '@/store';
import router from '@/router';

import moment from 'moment';

const API_BASE = process.env.VUE_APP_API_BASE || window.location.origin;
const API_URL= process.env.VUE_APP_API_URL || API_BASE + "/api/v1"


export const http = axios.create({
    baseURL: API_URL,
});

let refreshRegistration = -1;


// TODO: pull from cookie instead of store?
function refreshToken(config: AxiosRequestConfig) : any {
    if (store.getters['auth/hasToken']) {
        let token = store.getters['auth/getToken'];
        let expUtc = token.exp;
        let nowUtc  = moment.utc().unix()
        if (expUtc < nowUtc) {
            console.log("Token is Expired", expUtc, nowUtc)
            store.dispatch('auth/deauthenticate').then(() => {
                router.push({name: 'login'})
                return config
            })
        } else {
            let diff = expUtc - nowUtc;
            // expires in 5 minutes
            if (diff < 300) {
                console.log("Token is About to Expire", expUtc, nowUtc, diff)
                store.dispatch('auth/refresh').then(() => {
                    return config
                })
            } else {
                return config
            }
        }
    } else {
        return config
    }
}

function handleError(error: any) {
    return Promise.reject(error);
}

http.interceptors.request.use(refreshToken, handleError);

export function setServiceToken(jwt: string) {
    http.defaults.headers.common['Authorization'] = `Bearer ${jwt}`;
}

export function clearServiceToken() {
    delete http.defaults.headers.common['Authorization'];
}
