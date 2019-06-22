import qs from 'qs';
import * as api from '@/services/api';
import { LoginForm, UserResponse } from '@/types';

export interface TokenResponse {
    access_token: string;
    token_type: string;
    ws_access_token?: string;
}

class AuthService {
    refresh(token: string): Promise<string> {
        console.log('Sending refresh request for token');
        // must be form data for authentication
        return new Promise((resolve, reject) => {
            let http = api.makeHttp();
            http.defaults.headers.common['Authorization'] = `Bearer ${token}`;

            http.post('/auth/refresh', {})
                .then((response) => {
                    console.log('recieved valid refresh response', response);

                    // In this case, the websocket token is set on access token
                    const token = (response.data as TokenResponse).access_token;
                    resolve(token);
                })
                .catch((err) => {
                    console.log('recieved invalid refresh response', err);
                    reject(err);
                });
        });
    }

    login(form: LoginForm): Promise<any> {
        // must be form data for authentication
        return new Promise((resolve, reject) => {
            let headers = {
                'content-type': 'application/x-www-form-urlencoded',
            };
            let params = { ws_access_token: true };
            let data = qs.stringify(form);
            console.log('Sending login request');

            let http = api.makeHttp();

            http.post('/auth/token', data, {
                headers,
                params,
            })
                .then((response) => {
                    console.log('recieved valid login response', response);
                    const accessToken = (response.data as TokenResponse)
                        .access_token;
                    const wsAccessToken =
                        (response.data as TokenResponse).ws_access_token || '';
                    resolve({ accessToken, wsAccessToken });
                })
                .catch((err) => {
                    console.log('recieved invalid login response', err);
                    reject(err);
                });
        });
    }

    getUser(): Promise<UserResponse> {
        return new Promise((resolve, reject) => {
            let http = api.makeHttp();
            let request = http.get('/auth/user');
            return request
                .then((response) => {
                    resolve(response.data as UserResponse);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }
}

export default new AuthService();
