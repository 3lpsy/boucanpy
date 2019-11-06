export const API_BASE = process.env.VUE_APP_API_BASE || window.location.origin;
export const API_URL = process.env.VUE_APP_API_URL || API_BASE + '/api/v1';

let WS_PROTOCOL = '';

if (API_URL.lastIndexOf('https', 0) === 0) {
    WS_PROTOCOL = 'wss://';
} else {
    WS_PROTOCOL = 'ws://';
}
export const BROADCAST_BASE =
    process.env.VUE_APP_BROADCAST_BASE || WS_PROTOCOL + window.location.host;

export const BROADCAST_URL =
    process.env.VUE_APP_BROADCAST_URL || BROADCAST_BASE + '/broadcast';
