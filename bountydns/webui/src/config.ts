export const API_BASE = process.env.VUE_APP_API_BASE || window.location.origin;
export const API_URL = process.env.VUE_APP_API_URL || API_BASE + '/api/v1';

console.log('API_URL', API_URL);
export const BROADCAST_BASE =
    process.env.VUE_APP_BROADCAST_BASE || 'ws://' + window.location.host;

export const BROADCAST_URL =
    process.env.VUE_APP_BROADCAST_URL || BROADCAST_BASE + '/ws';

console.log('BROADCAST_URL', BROADCAST_URL);
