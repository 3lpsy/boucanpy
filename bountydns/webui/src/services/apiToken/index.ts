import qs from 'qs';
import * as api from '@/services/api'
import { ApiTokensResponse, ApiTokenResponse, ApiTokenCreateForm, SensitiveApiTokenResponse } from '@/types';


class ApiTokenService {
    getApiTokens(page: number = 1, perPage: number = 20): Promise<ApiTokensResponse> {
        return new Promise((resolve, reject) => {
            let query = qs.stringify({page: page, per_page: perPage});
            api.http.get('/api-token', {data: query}).then((response: any) => {
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
