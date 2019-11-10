import qs from 'qs';
import * as api from '@/services/api';
import { HttpRequestsResponse, HttpRequestResponse } from '@/types';

class HttpRequestService {
    getHttpRequests(
        page: number = 1,
        perPage: number = 20,
        sortBy: string = 'id',
        sortDir: string = 'asc',
        includes: string[] = [],
    ): Promise<HttpRequestsResponse> {
        return new Promise((resolve, reject) => {
            let query = {
                page: page,
                per_page: perPage,
                sort_by: sortBy,
                sort_dir: sortDir,
                includes: includes,
            };
            api.http
                .get('/http-request', { params: query })
                .then((response: any) => {
                    let responseData = response.data as HttpRequestsResponse;
                    resolve(responseData);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }

    getHttpRequest(
        httpRequestId: number,
        includes?: string[],
    ): Promise<HttpRequestResponse> {
        return new Promise((resolve, reject) => {
            let query = { includes: includes };
            api.http
                .get(`/http-request/${httpRequestId}`, { params: query })
                .then((response: any) => {
                    let data = response.data as HttpRequestResponse;
                    resolve(data);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }
}

export default new HttpRequestService();
