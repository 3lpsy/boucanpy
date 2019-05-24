import qs from 'qs';
import * as api from '@/services/api';
import {
    ApiTokensResponse,
    ApiTokenResponse,
    ApiTokenCreateForm,
    SensitiveApiTokenResponse,
} from '@/types';
import { IGeneralQS } from '@/queries';

class ApiTokenService {
    getApiTokens(query: IGeneralQS): Promise<ApiTokensResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .get('/api-token', { params: query })
                .then((response: any) => {
                    let responseData = response.data as ApiTokensResponse;
                    resolve(responseData);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }

    getApiToken(
        apiTokenId: number,
        includes?: string[],
    ): Promise<ApiTokenResponse> {
        return new Promise((resolve, reject) => {
            let query = { includes };
            api.http
                .get(`/api-token/${apiTokenId}`, { params: query })
                .then((response: any) => {
                    let responseData = response.data as ApiTokenResponse;
                    resolve(responseData);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }

    getSensitiveApiToken(tokenId: number, includes?: string[]) {
        return new Promise((resolve, reject) => {
            let query = { includes };
            api.http
                .get(`/api-token/${tokenId}/sensitive`, { params: query })
                .then((response: any) => {
                    let responseData = response.data as SensitiveApiTokenResponse;
                    resolve(responseData);
                })
                .catch((e) => reject(e));
        });
    }

    createApiToken(form: ApiTokenCreateForm): Promise<ApiTokenResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .post('/api-token', form)
                .then((response: any) => {
                    let responseData = response.data as ApiTokenResponse;
                    resolve(responseData);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }

    updateApiToken(
        apiTokenId: number,
        form: ApiTokenCreateForm,
    ): Promise<ApiTokenResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .put(`/api-token/${apiTokenId}`, form)
                .then((response: any) => {
                    let responseData = response.data as ApiTokenResponse;
                    resolve(responseData);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }

    deactivateApiToken(tokenId: number): Promise<any> {
        return new Promise((resolve, reject) => {
            api.http
                .delete(`/api-token/${tokenId}`)
                .then((response: any) => {
                    let responseData = response.data as ApiTokenResponse;
                    resolve(responseData);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }
}

export default new ApiTokenService();
