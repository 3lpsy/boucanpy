<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-12 col-xs-12">
                    <h2>Create Api Token</h2>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <api-token-form mode="create"></api-token-form>
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
export default class ApiTokenCreate extends Vue {}
</script>
