export const API_BASE = process.env.VUE_APP_API_BASE || window.location.origin;
export const API_URL = process.env.VUE_APP_API_URL || API_BASE + '/api/v1';

export const WS_BASE =
    process.env.VUE_APP_WS_BASE || 'ws://' + window.location.host;

export const WS_URL = process.env.VUE_APP_WS_URL || WS_BASE + '/ws';
