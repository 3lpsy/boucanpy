<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-12 col-xs-12">
                    <h2>Create DNS Server</h2>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <dns-server-form mode="create"></dns-server-form>
                </div>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import DnsServerForm from '@/components/dnsServer/DnsServerForm.vue';

@Component({ components: { DnsServerForm } })
export default class DnsServerCreate extends Vue {}
</script>
