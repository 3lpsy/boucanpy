import qs from 'qs';
import * as api from '@/services/api'
import { LoginForm, UserResponse } from '@/types';

export interface TokenResponse {
    access_token: string;
    token_type: string;
    ws_access_token?: string
}

class AuthService {
    refresh(): Promise<string> {
        // must be form data for authentication
        return new Promise((resolve, reject) => {
            let request = api.http.post('/auth/refresh')
            return request.then((response) => {
                const token = (response.data as TokenResponse).access_token
                resolve(token);
            }).catch((err) => {
                reject(err)
            })

        })
    }

    login(form: LoginForm): Promise<any> {
        // must be form data for authentication
        return new Promise((resolve, reject) => {
            let headers = { 'content-type': 'application/x-www-form-urlencoded' }
            let params = { ws_access_token: true }
            let data = qs.stringify(form);
            let config = {headers, params};
            let request = api.http.post('/auth/token', data, config);
            return request.then((response) => {
                console.log("recieved valid login response", response)
                const accessToken = (response.data as TokenResponse).access_token
                const wsAccessToken = (response.data as TokenResponse).ws_access_token || ''
                resolve({accessToken, wsAccessToken});
            }).catch((err) => {
                console.log("recieved invalid login response", err)
                reject(err)
            })

        })
    }

    getUser(): Promise<UserResponse> {
        return new Promise((resolve, reject) => {
            let request = api.http.get('/auth/user')
            return request.then((response) => {
                resolve((response.data as UserResponse))
            }).catch((err) => {
                reject(err)
            })
        })
    }
}

export default new AuthService();
