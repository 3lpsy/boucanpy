<template id="">
    <div class v-if="isAuthenticated">
        <b-table
            v-if="items.length > 0"
            no-local-sorting
            striped
            hover
            :items="items"
            :fields="fields"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
            v-on:sort-changed="changeSort"
        >
            <template v-slot:cell(actions)="row">
                <router-link
                    style="margin: 5px"
                    :to="{ name: 'http-request.show', params: { httpRequestId: row.item.id } }"
                    tag="button"
                    class="btn btn-info btn-sm"
                >View</router-link>
            </template>
            <template v-slot:cell(created_at)="row">{{ diffForHumans(moment(row.item.created_at))}}</template>
            <template v-slot:cell(http_server_name)="row">
                <span
                    v-if="row.item.http_server"
                >{{ truncateWithTrail(row.item.http_server.name, 10, '...') }}</span>
            </template>
        </b-table>
        <div class="col-xs-12 text-center" v-if="items.length < 1 && isLoaded">
            <span class="text-center">No Data Found :(</span>
        </div>

        <div class="col-xs-12 text-center" v-if="items.length < 1 && !isLoaded">
            <span class="text-center">Loading Data</span>
        </div>

        <b-pagination
            v-if="items.length > 0"
            v-model="currentPage"
            :total-rows="total"
            :per-page="perPage"
            aria-controls="my-table"
            @change="changePage"
        ></b-pagination>
    </div>
</template>

<script>
import Vue from 'vue';
import Component from 'vue-class-component';
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
import HttpRequestMixin from '@/mixins/httpRequest';
import httpRequest from '@/services/httpRequest';
import DataTableMixin from '@/mixins/dataTable';

// TODO: move to vuex / persistent data
@Component({})
export default class HttpRequestsTable extends mixins(
    CommonMixin,
    HttpRequestMixin,
    DataTableMixin,
) {
    sortBy = 'created_at';
    sortDesc = true;
    fields = [
        {
            key: 'id',
            label: 'ID',
            sortable: true,
        },
        { key: 'name', label: 'Name', sortable: true },
        {
            key: 'source_address',
            label: 'Source',
            sortable: true,
        },
        {
            key: 'type',

            label: 'Type',
            sortable: true,
        },
        {
            key: 'http_server_name',
            label: 'Server',
            sortable: false,
        },
        {
            key: 'zone_id',
            label: 'Zone',
            sortable: true,
        },
        {
            key: 'created_at',
            label: 'Created',
            sortable: true,
        },
        {
            key: 'actions',
            label: 'Actions',
        },
    ];
    loadData() {
        httpRequest
            .getHttpRequests(
                this.currentPage || 1,
                this.perPage,
                this.sortBy,
                this.sortDesc ? 'desc' : 'asc',
                ['http_server'],
            )
            .then((res) => {
                this.currentPage = res.pagination.page;
                this.perPage = res.pagination.per_page;
                this.total = res.pagination.total;
                this.items = res.http_requests;
                this.isLoaded = true;
            });
    }
    created() {
        this.registerOnBroadcastHttpRequestCreated();
    }
    mounted() {
        this.loadData();
    }
}
</script>
