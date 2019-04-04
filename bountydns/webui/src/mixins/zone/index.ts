// mixin.js
import Vue from 'vue';
import Component from 'vue-class-component';
import bus from  '@/bus'

// You can declare a mixin as the same style as components.
@Component
export default class ZoneMixin extends Vue {
    loadData() {

    }

    registerOnBroadcastZoneCreated() {
        console.log("registering WS_BROADCAST_MESSAGE for Zone")
        bus.$on("WS_BROADCAST_MESSAGE", (event: any) => {
            let message = event.message;
            if (message.name == "ZONE_CREATED") {
                this.loadData()
                bus.$emit('APP_ALERT', { text: 'New Zone Added!', type: 'info' });
            }

        })
    }
}
