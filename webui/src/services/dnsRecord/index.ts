import qs from 'qs';
import * as api from '@/services/api';
import {
    DnsRecordsResponse,
    DnsRecordResponse,
    DnsRecordsDigResponse,
    DnsRecordForZoneCreateForm,
    DnsRecordCreateForm,
} from '@/types';

import { IGeneralQS } from '@/queries';

class DnsRecordService {
    getDnsRecords(query: IGeneralQS): Promise<DnsRecordsResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .get(`/dns-record`, { params: query })
                .then((response: any) => {
                    let data = response.data as DnsRecordsResponse;
                    resolve(data);
                })
                .catch((e) => reject(e));
        });
    }
    getDnsRecordsForZone(
        zoneId: number,
        query: IGeneralQS,
    ): Promise<DnsRecordsResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .get(`/zone/${zoneId}/dns-record`, { params: query })
                .then((response: any) => {
                    let data = response.data as DnsRecordsResponse;
                    resolve(data);
                })
                .catch((e) => reject(e));
        });
    }

    getDnsRecordsDigForZone(zoneId: number): Promise<DnsRecordsDigResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .get(`/zone/${zoneId}/dns-record/dig`)
                .then((response: any) => {
                    let data = response.data as DnsRecordsDigResponse;
                    resolve(data);
                })
                .catch((e) => reject(e));
        });
    }

    getDnsRecord(
        dnsRecordId: number,
        includes?: string[],
    ): Promise<DnsRecordResponse> {
        let query = { includes };
        return new Promise((resolve, reject) => {
            api.http
                .get(`/dns-record/${dnsRecordId}`, {
                    params: query,
                })
                .then((response: any) => {
                    let data = response.data as DnsRecordResponse;
                    resolve(data);
                })
                .catch((e) => reject(e));
        });
    }

    getDnsRecordForZone(
        dnsRecordId: number,
        zoneId: number,
        includes?: string[],
    ): Promise<DnsRecordResponse> {
        let query = { includes };
        return new Promise((resolve, reject) => {
            api.http
                .get(`/zone/${zoneId}/dns-record/${dnsRecordId}`, {
                    params: query,
                })
                .then((response: any) => {
                    let data = response.data as DnsRecordResponse;
                    resolve(data);
                })
                .catch((e) => reject(e));
        });
    }

    createDnsRecord(form: DnsRecordCreateForm): Promise<DnsRecordResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .post(`/dns-record`, form)
                .then((response: any) => {
                    let data = response.data as DnsRecordResponse;
                    resolve(data);
                })
                .catch((e) => reject(e));
        });
    }

    createDnsRecordForZone(
        zoneId: number,
        form: DnsRecordForZoneCreateForm,
    ): Promise<DnsRecordResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .post(`/zone/${zoneId}/dns-record`, form)
                .then((response: any) => {
                    let data = response.data as DnsRecordResponse;
                    resolve(data);
                })
                .catch((e) => reject(e));
        });
    }
    // TODO: create update form type for dns record
    updateDnsRecord(
        dnsRecordId: number,
        form: DnsRecordCreateForm,
    ): Promise<DnsRecordResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .put(`/dns-record/${dnsRecordId}`, form)
                .then((response: any) => {
                    let data = response.data as DnsRecordResponse;
                    resolve(data);
                })
                .catch((e) => reject(e));
        });
    }

    // TODO: create update form type for dns record
    updateDnsRecordForZone(
        dnsRecordId: number,
        zoneId: number,
        form: DnsRecordForZoneCreateForm,
    ): Promise<DnsRecordResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .put(`/zone/${zoneId}/dns-record/${dnsRecordId}`, form)
                .then((response: any) => {
                    let data = response.data as DnsRecordResponse;
                    resolve(data);
                });
        });
    }

    destroyRecord(dnsRecordId: number): Promise<any> {
        return api.http.delete(`/dns-record/${dnsRecordId}`);
    }
}

export default new DnsRecordService();
