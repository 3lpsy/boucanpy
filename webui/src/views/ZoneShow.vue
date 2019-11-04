<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page" v-if="isLoaded">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-12 col-xs-12">
                    <h3 v-if="zoneId">Zone: {{ zoneId }}</h3>
                </div>
            </div>
            <div class="row" v-if="zone && zone.id">
                <div class="col-md-12 col-xs-12">
                    <strong>Domain:</strong>
                    {{ zone.domain }}
                </div>
                <div class="col-md-12 col-xs-12">
                    <strong>IP (Resolves To):</strong>
                    {{ zone.ip }}
                </div>
            </div>
            <br>
            <br>

            <div class="row" style="margin-bottom: 10px;" v-if="isLoaded">
                <div class="col-md-9 col-xs-12">
                    <h4>
                        DNS Records
                        <small style="font-size: .6em">
                            <a
                                v-on:click.stop.prevent="showDigModal"
                                :href="$route.fullPath"
                            >(View Records in Dig Format)</a>
                        </small>
                    </h4>
                </div>
                <div class="col-md-3 col-xs-12">
                    <router-link
                        tag="button"
                        class="btn pull-right btn-outline-primary"
                        :to="{
                            name: 'zone.dns-record.create',
                            params: { zoneId },
                        }"
                    >Create DNS Record</router-link>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <dns-records-table :zone-id="zoneId"></dns-records-table>
                </div>
            </div>
        </b-container>
        <b-modal
            v-model="digModalShow"
            id="show-dig-data"
            title="Dig Records"
            v-if="dig"
            size="lg"
            ok-only
        >
            <div class="col-xs-12">
                <span>
                    <code style="white-space: pre-line">{{ dig }}</code>
                </span>
            </div>
        </b-modal>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import zone from '@/services/zone';
import dnsRecord from '@/services/dnsRecord';
import DnsRecordsTable from '@/components/dnsRecord/DnsRecordsTable.vue';

@Component({
    components: { DnsRecordsTable },
})
export default class ZoneShow extends Vue {
    isLoaded = false;
    zone = {
        id: 0,
        domain: '',
        ip: '',
        is_active: false,
    };

    digModalShow = false;
    dig = '';

    showDigModal(e: any) {
        console.log('showingDigModal');
        dnsRecord.getDnsRecordsDigForZone(this.zoneId).then((res) => {
            this.dig = res.dig;
            this.digModalShow = true;
        });
    }

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

    boot() {
        // check to make sure dnsServer exists for edit form and load data
        zone.getZone(this.zoneId)
            .then((res) => {
                this.isLoaded = true;
                this.zone = res.zone;
            })
            .catch((e) => {
                console.log(e);
                throw e;
            });
    }

    mounted() {
        if (!this.zoneId) {
            this.$router.push({ name: 'home' });
        }
        this.boot();
    }
}
</script>
