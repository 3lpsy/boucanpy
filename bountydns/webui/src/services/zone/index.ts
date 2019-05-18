import qs from 'qs';
import * as api from '@/services/api'
import { ZonesResponse, ZoneResponse, ZoneCreateForm } from '@/types';


class ZoneService {
    getZones(page: number = 1, perPage: number = 20, sortBy: string = '', sortDir: string = 'asc', includes?: string[]): Promise<ZonesResponse> {
        return new Promise((resolve, reject) => {
            let query = {page: page, per_page: perPage, sort_by: sortBy, sort_dir: sortDir, includes: includes};
            api.http.get('/zone', {params: query}).then((response: any) => {
                let responseData = (response.data as ZonesResponse)
                resolve(responseData)
            }).catch((err) => {
                reject(err)
            })
        })
    }

    createZone(form: ZoneCreateForm): Promise<ZoneResponse> {
        return new Promise((resolve, reject) => {
            api.http.post('/zone', form).then((response: any) => {
                let responseData = (response.data as ZoneResponse)
                resolve(responseData)
            }).catch((err) => {
                reject(err)
            })
        })
    }

    deactivateZone(zoneId: number): Promise<any> {
        return new Promise((resolve, reject) => {
            api.http.delete(`/zone/${zoneId}`).then((response: any) => {
                let responseData = (response.data as ZoneResponse)
                resolve(responseData)
            }).catch((err) => {
                reject(err)
            })
        })
    }

    activateZone(zoneId: number): Promise<any> {
        return new Promise((resolve, reject) => {
            api.http.put(`/zone/${zoneId}/activate`).then((response: any) => {
                let responseData = (response.data as ZoneResponse)
                resolve(responseData)
            }).catch((err) => {
                reject(err)
            })
        })
    }
}

export default new ZoneService();
