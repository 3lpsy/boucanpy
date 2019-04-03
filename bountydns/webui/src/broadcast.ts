
import {BROADCAST_URL} from '@/config';

class Broadcast {
    publicWS: any = new WebSocket(BROADCAST_URL)
    authedWS: any

    authedWSOnOpen(event: any) {
        console.log("authed ws on open", event)

    }
    authedWSOnMessage(event: any) {
        console.log("authed ws on message", event)

    }

    registerAuthedWS(wsTokenRaw: string) {
        let url = BROADCAST_URL + '/' + wsTokenRaw;
        const authedWS = new WebSocket(url);
        this.authedWS = authedWS
        authedWS.onopen = this.authedWSOnOpen
        authedWS.onmessage = this.authedWSOnMessage
    }

    publicOnMessage(event: any) {
        let res = event.data;
        let data = JSON.parse(res)
        console.log("onmessage", data)
    };

    publicOnOpen(event: any) {
        console.log("onopen", event)
        let msg = {message: 'yo'}
        this.publicWS.send(JSON.stringify(msg))
    }

    registerPublicWS() {
        this.publicWS.onmessage = this.publicOnMessage
        this.publicWS.onopen = this.publicOnOpen
    }

}

export default new Broadcast()
