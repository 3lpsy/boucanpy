<template id="">
    <div class v-if="isAuthenticated">
        <b-table
            v-if="items.length > 0"
            striped
            hover
            :items="items"
            :fields="fields"
            :sort-by.sync="query.sort_by"
            :sort-desc="query.sort_dir == 'desc'"
            v-on:sort-changed="changeSort"
            :busy="isLoading || !isLoaded"
        >
            <template v-slot:cell(actions)="row">
                <div>
                    <router-link
                        style="margin: 5px"
                        :to="{ name: 'http-server.edit', params: { httpServerId: row.item.id } }"
                        tag="button"
                        class="btn btn-warning btn-sm"
                    >Edit</router-link>
                    <router-link
                        style="margin: 5px"
                        :to="{ name: 'http-server.show', params: { httpServerId: row.item.id } }"
                        tag="button"
                        class="btn btn-info btn-sm"
                    >View</router-link>
                </div>
            </template>
            <template v-slot:cell(created_at)="row">{{ diffForHumans(moment(row.item.created_at))}}</template>
            <template v-slot:cell(zones)="row">
                <span v-for="(zone, index) in row.item.zones" :key="index">
                    {{zone.domain}}
                    <span v-if="index+1 != row.item.zones.length">,</span>
                </span>
            </template>
        </b-table>
        <div class="col-xs-12 text-center" v-if="items.length < 1 && isLoaded">
            <span class="text-center">No Data Found :(</span>
        </div>

        <div class="col-xs-12 text-center" v-if="items.length < 1 && !isLoaded">
            <span class="text-center">Loading Data</span>
        </div>

        <b-pagination
            v-if="query.page > 0 && items.length > 0"
            v-model="query.page"
            :total-rows="total"
            :per-page="query.per_page"
            aria-controls="my-table"
            @change="changePage"
            style="margin-top:10px;"
        ></b-pagination>
    </div>
</template>

<script>
import Vue from 'vue';
import Component from 'vue-class-component';
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
import DataTableMixin from '@/mixins/dataTable';
import httpServer from '@/services/httpServer';
import bus from '@/bus';
import { GeneralQS } from '@/queries';

// TODO: move to vuex / persistent data
@Component({})
export default class HttpServersTable extends mixins(
    CommonMixin,
    DataTableMixin,
) {
    items = [];
    query = new GeneralQS();
    isLoading = false;
    isLoaded = false;
    fields = [
        {
            key: 'id',
            label: 'ID',
            sortable: true,
        },
        {
            key: 'name',
            label: 'Name',
            sortable: true,
        },
        {
            key: 'zones',
            label: 'Zones',
            sortable: false,
        },
        {
            key: 'created_at',
            label: 'Created At',
            sortable: true,
        },
        {
            key: 'actions',
            label: 'Actions',
        },
    ];

    changeSort(sort) {
        this.query.sort_by = sort.sortBy;
        if (sort.sortDesc) {
            this.query.sort_dir = 'desc';
        } else {
            this.query.sort_dir = 'asc';
        }
        this.loadData();
    }

    loadData() {
        this.isLoading = true;
        this.query.includes = ['zones'];
        return httpServer.getHttpServers(this.query).then((res) => {
            let query = new GeneralQS();
            query.page = res.pagination.page;
            query.per_page = res.pagination.per_page;
            query.sort_by = this.query.sort_by;
            query.sort_dir = this.query.sort_dir;
            this.query = query;
            this.total = res.pagination.total;
            this.items = res.http_servers;
            this.isLoaded = true;
            this.isLoading = false;
        });
    }

    freshLoad() {
        this.loadData();
    }

    mounted() {
        this.freshLoad();
        bus.$on('HTTP_SERVER_ADDED', (payload) => {
            this.freshLoad();
        });
    }
}
</script>
