<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-12 col-xs-12">
                    <h2 v-if="apiTokenId">Edit Api Token: {{ apiTokenId }}</h2>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <api-token-form mode="edit" :api-token-id="apiTokenId"></api-token-form>
                </div>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import ApiTokenForm from '@/components/apiToken/ApiTokenForm.vue';

@Component({ components: { ApiTokenForm } })
export default class ApiTokenEdit extends Vue {
    get apiTokenId() {
        if (!this.$route.params || !this.$route.params.apiTokenId) {
            return 0;
        }
        try {
            return parseInt(this.$route.params.apiTokenId);
        } catch (e) {
            return 0;
        }
    }

    mounted() {
        if (!this.apiTokenId) {
            this.$router.push({ name: 'home' });
        }
    }
}
</script>
