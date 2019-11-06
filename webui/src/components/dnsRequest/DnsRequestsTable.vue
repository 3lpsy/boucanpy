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
        ></b-table>
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
import DnsRequestMixin from '@/mixins/dnsRequest';
import dnsRequest from '@/services/dnsRequest';
import DataTableMixin from '@/mixins/dataTable';

// TODO: move to vuex / persistent data
@Component({})
export default class DnsRequestsTable extends mixins(
    CommonMixin,
    DnsRequestMixin,
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
        {
            key: 'dns_server_name',
            label: 'Server',
            sortable: true,
        },
        {
            key: 'zone_id',
            label: 'Zone',
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
            key: 'created_at',
            label: 'Created',
            sortable: true,
            formatter: 'formatDate',
        },
    ];
    loadData() {
        dnsRequest
            .getDnsRequests(
                this.currentPage || 1,
                this.perPage,
                this.sortBy,
                this.sortDesc ? 'desc' : 'asc',
            )
            .then((res) => {
                this.currentPage = res.pagination.page;
                this.perPage = res.pagination.per_page;
                this.total = res.pagination.total;
                this.items = res.dns_requests;
                this.isLoaded = true;
            });
    }
    created() {
        this.registerOnBroadcastDnsRequestCreated();
    }
    mounted() {
        this.loadData();
    }
}
</script>
