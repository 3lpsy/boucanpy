<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-12 col-xs-12">
                    <h2 v-if="dnsServerId">Edit DNS Server: {{ dnsServerId }}</h2>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <dns-server-form mode="edit" :dns-server-id="dnsServerId"></dns-server-form>
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
export default class DnsServerEdit extends Vue {
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

    mounted() {
        if (!this.dnsServerId) {
            this.$router.push({ name: 'home' });
        }
    }
}
</script>
