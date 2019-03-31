import qs from 'qs';
import * as api from '@/services/api'
import { LoginForm, UserResponse } from '@/types';

export interface TokenResponse {
    access_token: string;
    token_type: string
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

    login(form: LoginForm): Promise<string> {
        // must be form data for authentication
        return new Promise((resolve, reject) => {
            let headers = { 'content-type': 'application/x-www-form-urlencoded' }
            let data = qs.stringify(form)
            let request = api.http.post('/auth/token', data, {headers})
            return request.then((response) => {
                console.log("recieved valid login response", response)
                const token = (response.data as TokenResponse).access_token
                resolve(token);
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
