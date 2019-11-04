<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-9 col-xs-12">
                    <h2>Zones</h2>
                </div>
                <div class="col-md-3 col-xs-12">
                    <router-link
                        tag="button"
                        class="btn pull-right btn-outline-primary"
                        :to="{ name: 'zone.create' }"
                    >Create Zone</router-link>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <zones-table></zones-table>
                </div>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import ZonesTable from '@/components/zone/ZonesTable.vue';

@Component({ components: { ZonesTable } })
export default class Zone extends Vue {}
</script>
