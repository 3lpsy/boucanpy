<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-9 col-xs-12">
                    <h3 v-if="zoneId">
                        Create DNS Record
                        <small>Zone: {{zoneId}}</small>
                    </h3>
                </div>
            </div>

            <div class="row">
                <div
                    class="col-md-12 col-xs-12"
                    v-if="zoneId && zoneId > 0 && dnsRecordId && dnsRecordId > 0"
                >
                    <dns-record-form mode="edit" :zone-id="zoneId" :dns-record-id="dnsRecordId"></dns-record-form>
                </div>
            </div>
            <br>
            <br>
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-9 col-xs-12">
                    <h4 v-if="zoneId">Other DNS Records</h4>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12" v-if="zoneId">
                    <dns-records-table :zone-id="zoneId"></dns-records-table>
                </div>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import DnsRecordForm from '@/components/dnsRecord/DnsRecordForm.vue';
import DnsRecordsTable from '@/components/dnsRecord/DnsRecordsTable.vue';

@Component({ components: { DnsRecordForm, DnsRecordsTable } })
export default class ZoneDnsRecordEdit extends Vue {
    isLoading = true;
    isLoaded = false;

    get zoneId() {
        if (!this.$route.params || !this.$route.params.zoneId) {
            return 0;
        }
        try {
            return parseInt(this.$route.params.zoneId);
        } catch (e) {
            return 0;
        }
    }

    get dnsRecordId() {
        if (!this.$route.params || !this.$route.params.dnsRecordId) {
            return 0;
        }
        try {
            return parseInt(this.$route.params.dnsRecordId);
        } catch (e) {
            return 0;
        }
    }

    mounted() {
        if (!this.zoneId || !this.dnsRecordId) {
            this.$router.push({ name: 'home' });
        }
        this.isLoaded = true;
    }
}
</script>
