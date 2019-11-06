<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page" v-if="isLoaded">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-12 col-xs-12">
                    <h3 v-if="dnsRequestId">DNS Request: {{ dnsRequestId }}</h3>
                </div>
            </div>
            <div class="row" v-if="dnsRequest && dnsRequest.id"></div>
            <div v-if="dnsRequest && dnsRequest.id > 0">
                <b-card :title="dnsRequest.name" :sub-title="dnsRequest.source_address">
                    <b-card-text>
                        <strong>Received:</strong>
                        {{ moment(dnsRequest.created_at).format("YYYY-MM-DD HH:mm:ss") }}
                        <em>({{ diffForHumans(moment(dnsRequest.created_at))}})</em>
                    </b-card-text>
                    <b-card-text>
                        <strong>Type:</strong>
                        {{ dnsRequest.type}}
                    </b-card-text>
                    <b-card-text>
                        <strong>Raw Request:</strong>
                        <br>
                        <code style="white-space: pre-line">{{ dnsRequest.raw_request }}</code>
                    </b-card-text>
                </b-card>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import { mixins } from 'vue-class-component';

import dnsRequest from '@/services/dnsRequest';
import { DnsRequest } from '@/types';
import CommonMixin from '../mixins/common';

@Component
export default class DnsRequestShow extends mixins(CommonMixin) {
    isLoaded = false;
    dnsRequest: DnsRequest = {
        id: 0,
        name: '',
        zone_id: null,
        source_address: '',
        source_port: 0,
        type: '',
        protocol: '',
        dns_server_id: 0,
        created_at: 0,
        raw_request: '',
    };

    get dnsRequestId() {
        if (!this.$route.params || !this.$route.params.dnsRequestId) {
            return 0;
        }
        try {
            return parseInt(this.$route.params.dnsRequestId);
        } catch (e) {
            return 0;
        }
    }

    boot() {
        // check to make sure dnsServer exists for edit form and load data
        dnsRequest
            .getDnsRequest(this.dnsRequestId, ['zone', 'dns_server'])
            .then((res) => {
                this.isLoaded = true;
                this.dnsRequest = res.dns_request;
            })
            .catch((e) => {
                console.log(e);
                throw e;
            });
    }

    mounted() {
        if (!this.dnsRequestId) {
            this.$router.push({ name: 'home' });
        }
        this.boot();
    }
}
</script>
