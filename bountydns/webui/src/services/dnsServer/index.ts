import qs from 'qs';
import * as api from '@/services/api';
import { DnsServersResponse } from '@/types';

class DnsServerService {
    getDnsServers(
        page: number = 1,
        perPage: number = 20,
    ): Promise<DnsServersResponse> {
        return new Promise((resolve, reject) => {
            let query = qs.stringify({ page: page, per_page: perPage });
            api.http
                .get('/dns-server', { data: query })
                .then((response: any) => {
                    let responseData = response.data as DnsServersResponse;
                    resolve(responseData);
                });
        });
    }
}

export default new DnsServerService();
