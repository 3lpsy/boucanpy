import qs from 'qs';
import * as api from '@/services/api';
import { DnsRequestsResponse, DnsRequestResponse } from '@/types';

class DnsRequestService {
    getDnsRequests(
        page: number = 1,
        perPage: number = 20,
        sortBy: string = 'id',
        sortDir: string = 'asc',
        includes: string[] = [],
    ): Promise<DnsRequestsResponse> {
        return new Promise((resolve, reject) => {
            let query = {
                page: page,
                per_page: perPage,
                sort_by: sortBy,
                sort_dir: sortDir,
                includes: includes,
            };
            api.http
                .get('/dns-request', { params: query })
                .then((response: any) => {
                    let responseData = response.data as DnsRequestsResponse;
                    resolve(responseData);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }

    getDnsRequest(
        dnsRequestId: number,
        includes?: string[],
    ): Promise<DnsRequestResponse> {
        return new Promise((resolve, reject) => {
            let query = { includes: includes };
            api.http
                .get(`/dns-request/${dnsRequestId}`, { params: query })
                .then((response: any) => {
                    let data = response.data as DnsRequestResponse;
                    resolve(data);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }
}

export default new DnsRequestService();
