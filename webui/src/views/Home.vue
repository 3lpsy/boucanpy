<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row" style="padding-bottom: 10px">
                <div class="col-md-12 col-xs-12">
                    <h2>Dns Requests</h2>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <dns-requests-table></dns-requests-table>
                </div>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import DnsRequestsTable from '@/components/dnsRequest/DnsRequestsTable.vue';

@Component({ components: { DnsRequestsTable } })
export default class Home extends Vue {}
</script>
