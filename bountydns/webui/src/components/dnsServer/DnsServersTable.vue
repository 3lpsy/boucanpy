<template id="">
    <div class="" v-if="isAuthenticated">
        <b-table
            v-if="items.length > 0"
            striped
            hover
            :items="items"
            :fields="fields"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
            v-on:sort-changed="changeSort"
        >
        </b-table>
        <div class="col-xs-12 text-center" v-if="items.length < 1 && isLoaded">
            <span class="text-center">No Data Found :(</span>
        </div>

        <div class="col-xs-12 text-center" v-if="items.length < 1 && !isLoaded">
            <span class="text-center">Loading Data</span>
        </div>

        <b-pagination
            v-if="currentPage > 0 && items.length > 0"
            v-model="currentPage"
            :total-rows="total"
            :per-page="perPage"
            aria-controls="my-table"
            @change="changePage"
        ></b-pagination>
    </div>
</template>

<script>
import { Vue, Component } from 'vue-property-decorator';
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
import DnsServerMixin from '@/mixins/dnsServer';
import DataTableMixin from '@/mixins/dataTable';
import dnsServer from '@/services/dnsServer';
import bus from '@/bus';

// TODO: move to vuex / persistent data
@Component
export default class DnsServersTable extends mixins(
    CommonMixin,
    DnsServerMixin,
    DataTableMixin,
) {
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
        }
    ];


    loadData() {
        return dnsServer.getDnsServers(this.currentPage || 1, this.perPage, this.sortBy, this.sortDesc ? 'desc' : 'asc').then((res) => {
            this.currentPage = res.pagination.page;
            this.perPage = res.pagination.per_page;
            this.total = res.pagination.total;
            this.items = res.dns_servers;
            this.isLoaded = true;
        });
    }

    freshLoad() {
        this.loadData()
    }

    mounted() {
        this.freshLoad();
        bus.$on('DNS_SERVER_ADDED', (payload) => {
            this.freshLoad();
        });
    }
}
</script>
