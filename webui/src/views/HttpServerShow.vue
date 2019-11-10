<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page" v-if="isLoaded">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-12 col-xs-12">
                    <h2 v-if="httpServerId">HTTP Server: {{ httpServerId }}</h2>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12">Name: {{ httpServer.name }}</div>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import HttpServerForm from '@/components/httpServer/HttpServerForm.vue';

import httpServer from '@/services/httpServer';

@Component({ components: { HttpServerForm } })
export default class HttpServerShow extends Vue {
    isLoaded = false;
    httpServer = {
        name: '',
    };

    get httpServerId() {
        if (!this.$route.params || !this.$route.params.httpServerId) {
            return 0;
        }
        try {
            return parseInt(this.$route.params.httpServerId);
        } catch (e) {
            return 0;
        }
    }

    boot() {
        // check to make sure httpServer exists for edit form and load data
        httpServer
            .getHttpServer(this.httpServerId)
            .then((res) => {
                this.isLoaded = true;
                this.httpServer = res.http_server;
            })
            .catch((e) => {
                console.log(e);
                throw e;
            });
    }

    mounted() {
        if (!this.httpServerId) {
            this.$router.push({ name: 'home' });
        }
        this.boot();
    }
}
</script>
