import axios from 'axios';

const API_BASE = process.env.VUE_APP_API_BASE || window.location.origin;
const API_URL= process.env.VUE_APP_API_URL || API_BASE + "/api/v1"


export const http = axios.create({
    baseURL: API_URL,
});


export function setServiceToken(jwt: string) {
    http.defaults.headers.common['Authorization'] = `Bearer ${jwt}`;
}

export function clearServiceToken(jwt: string) {
    delete http.defaults.headers.common['Authorization'];
}
