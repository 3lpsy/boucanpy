<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page" v-if="isLoaded">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-12 col-xs-12">
                    <h3
                        v-if="httpRequestId"
                    >{{httpRequest.protocol.toUpperCase()}} Request: {{ httpRequestId }}</h3>
                </div>
            </div>
            <div class="row" v-if="httpRequest && httpRequest.id"></div>
            <div v-if="httpRequest && httpRequest.id > 0">
                <b-card :title="httpRequest.name" :sub-title="httpRequest.source_address">
                    <b-card-text>
                        <strong>Received:</strong>
                        {{ moment(httpRequest.created_at).format("YYYY-MM-DD HH:mm:ss") }}
                        <em>({{ diffForHumans(moment(httpRequest.created_at))}})</em>
                    </b-card-text>
                    <b-card-text>
                        <strong>Protocol:</strong>
                        {{ httpRequest.protocol}}
                    </b-card-text>
                    <b-card-text>
                        <strong>Type:</strong>
                        {{ httpRequest.type}}
                    </b-card-text>
                    <b-card-text>
                        <strong>Raw Request:</strong>
                        <br>
                        <code style="white-space: pre-line">{{ httpRequest.raw_request }}</code>
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

import httpRequest from '@/services/httpRequest';
import { HttpRequest } from '@/types';
import CommonMixin from '../mixins/common';

@Component
export default class HttpRequestShow extends mixins(CommonMixin) {
    isLoaded = false;
    httpRequest: HttpRequest = {
        id: 0,
        name: '',
        path: '',
        zone_id: null,
        source_address: '',
        source_port: 0,
        type: '',
        protocol: '',
        http_server_id: 0,
        created_at: 0,
        raw_request: '',
    };

    get httpRequestId() {
        if (!this.$route.params || !this.$route.params.httpRequestId) {
            return 0;
        }
        try {
            return parseInt(this.$route.params.httpRequestId);
        } catch (e) {
            return 0;
        }
    }

    boot() {
        // check to make sure httpServer exists for edit form and load data
        httpRequest
            .getHttpRequest(this.httpRequestId, ['zone', 'http_server'])
            .then((res) => {
                this.isLoaded = true;
                this.httpRequest = res.http_request;
            })
            .catch((e) => {
                console.log(e);
                throw e;
            });
    }

    mounted() {
        if (!this.httpRequestId) {
            this.$router.push({ name: 'home' });
        }
        this.boot();
    }
}
</script>
