<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row" style="padding-bottom: 10px">
                <div class="col-md-12 col-xs-12">
                    <h2>Activity</h2>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <b-tabs
                        content-class="mt-3"
                        justified
                        active-nav-item-class="font-weight-bold text-uppercase text-primary"
                    >
                        <b-tab title="DNS Requests" active>
                            <dns-requests-table></dns-requests-table>
                        </b-tab>
                        <b-tab title="HTTP Requests">
                            <http-requests-table></http-requests-table>
                        </b-tab>
                    </b-tabs>
                </div>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import DnsRequestsTable from '@/components/dnsRequest/DnsRequestsTable.vue';
import HttpRequestsTable from '@/components/httpRequest/HttpRequestsTable.vue';

@Component({ components: { DnsRequestsTable, HttpRequestsTable } })
export default class Home extends Vue {}
</script>
