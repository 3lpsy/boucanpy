<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page" v-if="isLoaded">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-12 col-xs-12">
                    <h2 v-if="dnsServerId">DNS Server: {{ dnsServerId }}</h2>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12">Name: {{ dnsServer.name }}</div>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import DnsServerForm from '@/components/dnsServer/DnsServerForm.vue';

import dnsServer from '@/services/dnsServer';

@Component({ components: { DnsServerForm } })
export default class DnsServerShow extends Vue {
    isLoaded = false;
    dnsServer = {
        name: '',
    };

    get dnsServerId() {
        if (!this.$route.params || !this.$route.params.dnsServerId) {
            return 0;
        }
        try {
            return parseInt(this.$route.params.dnsServerId);
        } catch (e) {
            return 0;
        }
    }

    boot() {
        // check to make sure dnsServer exists for edit form and load data
        dnsServer
            .getDnsServer(this.dnsServerId)
            .then((res) => {
                this.isLoaded = true;
                this.dnsServer = res.dns_server;
            })
            .catch((e) => {
                console.log(e);
                throw e;
            });
    }

    mounted() {
        if (!this.dnsServerId) {
            this.$router.push({ name: 'home' });
        }
        this.boot();
    }
}
</script>
