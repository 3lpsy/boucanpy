<template>
    <div class="page home-page row">
        <!-- <router-link
                        tag="button"
                        class="btn pull-right btn-outline-primary"
                        :to="{name: 'dns-server.create'}"
        >Create DNS Server</router-link>-->
        <b-container style="padding-top: 10px" class="page">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-8 col-xs-12">
                    <h2>Servers</h2>
                </div>

                <div class="col-md-4 col-xs-12">
                    <router-link
                        style="margin-left:5px"
                        tag="button"
                        class="btn pull-right btn-outline-primary"
                        :to="{name: 'dns-server.create'}"
                    >Create DNS Server</router-link>
                    <router-link
                        tag="button"
                        class="btn pull-right btn-outline-primary"
                        :to="{name: 'http-server.create'}"
                    >Create HTTP Server</router-link>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <b-tabs
                        content-class="mt-3"
                        justified
                        active-nav-item-class="font-weight-bold text-uppercase text-primary"
                    >
                        <b-tab title="DNS Servers" active>
                            <div class="row">
                                <div class="col-md-12 col-xs-12">
                                    <dns-servers-table></dns-servers-table>
                                </div>
                            </div>
                        </b-tab>
                        <b-tab title="HTTP Servers">
                            <div class="row">
                                <div class="col-md-12 col-xs-12">
                                    <http-servers-table></http-servers-table>
                                </div>
                            </div>
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
import DnsServersTable from '@/components/dnsServer/DnsServersTable.vue';
import HttpServersTable from '@/components/httpServer/HttpServersTable.vue';

@Component({ components: { DnsServersTable, HttpServersTable } })
export default class Server extends Vue {}
</script>
