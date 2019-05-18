import qs from 'qs';
import * as api from '@/services/api';
import { DnsServersResponse} from '@/types';

import {IGeneralQS} from "@/queries"
class DnsServerService {
    getDnsServers(query: IGeneralQS): Promise<DnsServersResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .get('/dns-server', { params: query })
                .then((response: any) => {
                    let responseData = response.data as DnsServersResponse;
                    resolve(responseData);
                });
        });
    }
}

export default new DnsServerService();
