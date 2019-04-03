
import {BROADCAST_URL} from '@/config';

export const publicWS = new WebSocket(BROADCAST_URL);

publicWS.onmessage = function(event) {
    let res = event.data;
    let data = JSON.parse(res)
    console.log("onmessage", data)

};

publicWS.onopen = function(event) {
    console.log("onopen", event)
    let msg = {message: 'yo'}
    publicWS.send(JSON.stringify(msg))
}

// TODO: add authed token
