import qs from 'qs';
import * as api from '@/services/api';
import {
    DnsServersResponse,
    DnsServerResponse,
    DnsServerCreateForm,
} from '@/types';

import { IGeneralQS } from '@/queries';

class DnsServerService {
    getDnsServers(query: IGeneralQS): Promise<DnsServersResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .get('/dns-server', { params: query })
                .then((response: any) => {
                    let data = response.data as DnsServersResponse;
                    resolve(data);
                })
                .catch((e) => reject(e));
        });
    }

    createDnsServer(form: DnsServerCreateForm): Promise<DnsServerResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .post('/dns-server', form)
                .then((response: any) => {
                    let data = response.data as DnsServerResponse;
                    resolve(data);
                })
                .catch((e) => reject(e));
        });
    }

    getDnsServer(
        dnsServerId: number,
        includes?: string[],
    ): Promise<DnsServerResponse> {
        return new Promise((resolve, reject) => {
            let query = { includes: includes };
            api.http
                .get(`/dns-server/${dnsServerId}`, { params: query })
                .then((response: any) => {
                    let data = response.data as DnsServerResponse;
                    resolve(data);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }

    updateDnsServer(
        dnsServerId: number,
        form: DnsServerCreateForm,
    ): Promise<DnsServerResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .put(`/dns-server/${dnsServerId}`, form)
                .then((response: any) => {
                    let data = response.data as DnsServerResponse;
                    resolve(data);
                })
                .catch((e) => reject(e));
        });
    }
}

export default new DnsServerService();
