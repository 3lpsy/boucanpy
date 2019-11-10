import qs from 'qs';
import * as api from '@/services/api';
import {
    HttpServersResponse,
    HttpServerResponse,
    HttpServerCreateForm,
} from '@/types';

import { IGeneralQS } from '@/queries';

class HttpServerService {
    getHttpServers(query: IGeneralQS): Promise<HttpServersResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .get('/http-server', { params: query })
                .then((response: any) => {
                    let data = response.data as HttpServersResponse;
                    resolve(data);
                })
                .catch((e) => reject(e));
        });
    }

    createHttpServer(form: HttpServerCreateForm): Promise<HttpServerResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .post('/http-server', form)
                .then((response: any) => {
                    let data = response.data as HttpServerResponse;
                    resolve(data);
                })
                .catch((e) => reject(e));
        });
    }

    getHttpServer(
        httpServerId: number,
        includes?: string[],
    ): Promise<HttpServerResponse> {
        return new Promise((resolve, reject) => {
            let query = { includes: includes };
            api.http
                .get(`/http-server/${httpServerId}`, { params: query })
                .then((response: any) => {
                    let data = response.data as HttpServerResponse;
                    resolve(data);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }

    updateHttpServer(
        httpServerId: number,
        form: HttpServerCreateForm,
    ): Promise<HttpServerResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .put(`/http-server/${httpServerId}`, form)
                .then((response: any) => {
                    let data = response.data as HttpServerResponse;
                    resolve(data);
                })
                .catch((e) => reject(e));
        });
    }
}

export default new HttpServerService();
