<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <h2>Servers</h2>
                </div>
            </div>
            <div class="row" style="padding-bottom: 20px">
                <div class="col-md-12 col-xs-12">
                    <b-button
                        v-b-modal.create-dns-server
                        class="pull-right"
                        variant="outline-primary"
                    >
                        Create DNS Server
                    </b-button>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <dns-server-table></dns-server-table>
                </div>
            </div>
        </b-container>
        <dns-server-create-modal modal-id="create-dns-server">
        </dns-server-create-modal>
    </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import DnsServerTable from '@/components/dnsServer/DnsServerTable.vue';
import DnsServerCreateModal from '@/components/dnsServer/DnsServerCreateModal.vue';

@Component({ components: { DnsServerTable, DnsServerCreateModal } })
export default class Home extends Vue {}
</script>
