<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-12 col-xs-12">
                    <h2 v-if="httpServerId">Edit HTTP Server: {{ httpServerId }}</h2>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <http-server-form mode="edit" :http-server-id="httpServerId"></http-server-form>
                </div>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import HttpServerForm from '@/components/httpServer/HttpServerForm.vue';

@Component({ components: { HttpServerForm } })
export default class HttpServerEdit extends Vue {
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

    mounted() {
        if (!this.httpServerId) {
            this.$router.push({ name: 'home' });
        }
    }
}
</script>
