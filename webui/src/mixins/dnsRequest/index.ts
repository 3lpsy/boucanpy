// mixin.js
import Vue from 'vue';
import Component from 'vue-class-component';
import bus from '@/bus';
// You can declare a mixin as the same style as components.
@Component
export default class DnsRequestMixin extends Vue {
    registeredEvents = [];
    loadData() {}
    registerOnBroadcastDnsRequestCreated() {
        console.log('registering DNS_REQUEST_CREATED on dns request table');
        bus.$on('DNS_REQUEST_CREATED', (event: any) => {
            this.loadData();
        });
    }
}
