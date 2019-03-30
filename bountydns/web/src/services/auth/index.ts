import qs from 'qs';
import * as api from '@/services/api'
import { LoginForm } from '@/types';

export interface TokenResponse {
    access_token: string;
    token_type: string
}

class AuthService {
    async login(form: LoginForm): Promise<string> {
        // must be form data for authentication
        let headers = { 'content-type': 'application/x-www-form-urlencoded' }
        let data = qs.stringify(form)
        const response = await api.http.post('/auth/token', data, {headers});
        return (response.data as TokenResponse).access_token;
    }
}

export default new AuthService();
