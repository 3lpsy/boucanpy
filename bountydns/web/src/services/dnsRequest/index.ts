import qs from 'qs';
import * as api from '@/services/api'
import { DnsRequestsResponse } from '@/types';

class DnsRequestService {
    getDnsRequests(page: number = 1, perPage: number = 20): Promise<DnsRequestsResponse> {
        return new Promise((resolve, reject) => {
            let query = qs.stringify({page: page, per_page: perPage});
            api.http.get('/dns-request', {data: query}).then((response: any) => {
                let responseData = (response.data as DnsRequestsResponse)
                resolve(responseData)
            }).catch((err) => {
                reject(err)
            })
        })
    }
}

export default new DnsRequestService();
