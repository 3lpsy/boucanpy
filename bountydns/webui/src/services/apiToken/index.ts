import qs from 'qs';
import * as api from '@/services/api'
import { ApiTokensResponse, ApiTokenResponse, ApiTokenCreateForm, SensitiveApiTokenResponse } from '@/types';


class ApiTokenService {
    getApiTokens(page: number = 1, perPage: number = 20, sortBy: string = 'id', sortDir: string = 'asc'): Promise<ApiTokensResponse> {
        return new Promise((resolve, reject) => {
            let query = {page: page, per_page: perPage, sort_by: sortBy, sort_dir: sortDir};
            api.http.get('/api-token', {params: query}).then((response: any) => {
                let responseData = (response.data as ApiTokensResponse)
                resolve(responseData)
            }).catch((err) => {
                reject(err)
            })
        })
    }

    getSensitiveApiToken(tokenId: number) {
        return new Promise((resolve, reject) => {
            api.http.get(`/api-token/${tokenId}/sensitive`).then((response: any) => {
                let responseData = (response.data as SensitiveApiTokenResponse)
                resolve(responseData)
            })
        })
    }

    createApiToken(form: ApiTokenCreateForm): Promise<ApiTokenResponse> {
        return new Promise((resolve, reject) => {
            api.http.post('/api-token', form).then((response: any) => {
                let responseData = (response.data as ApiTokenResponse)
                resolve(responseData)
            }).catch((err) => {
                reject(err)
            })
        })
    }

    deactivateApiToken(tokenId: number): Promise<any> {
        return new Promise((resolve, reject) => {
            api.http.delete(`/api-token/${tokenId}`).then((response: any) => {
                let responseData = (response.data as ApiTokenResponse)
                resolve(responseData)
            }).catch((err) => {
                reject(err)
            })
        })
    }
}

export default new ApiTokenService();
