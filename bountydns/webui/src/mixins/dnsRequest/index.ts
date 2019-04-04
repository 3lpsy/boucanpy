// mixin.js
import Vue from 'vue';
import Component from 'vue-class-component';
import bus from  '@/bus'
// You can declare a mixin as the same style as components.
@Component
export default class DnsRequestMixin extends Vue {

    loadData() {

    }
    mounted() {
        this.loadData()
        bus.$on("WS_BROADCAST_MESSAGE", (event: any) => {
            let message = event.message;
            if (message.name == "DNS_REQUEST_CREATED") {
                this.loadData()
                bus.$emit('APP_ALERT', { text: 'New DNS Request Added!', type: 'info' });
            }

        })
    }
}
