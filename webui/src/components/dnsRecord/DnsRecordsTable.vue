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
                <b-button size="sm" @click="destroyRecord(row.item)">Delete</b-button>
                <b-button-group>
                    <router-link
                        :to="getEditLink(row.item)"
                        tag="button"
                        class="btn btn-info btn-sm"
                    >Edit</router-link>
                </b-button-group>
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
import Component from 'vue-class-component';
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
import DataTableMixin from '@/mixins/dataTable';
import dnsRecord from '@/services/dnsRecord';
import bus from '@/bus';
import { GeneralQS } from '@/queries';

// TODO: move to vuex / persistent data
@Component({
    props: {
        zoneId: {
            type: Number,
            default: 0,
        },
    },
})
export default class DnsRecordsTable extends mixins(
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
            key: 'record',
            label: 'Record',
            sortable: true,
        },
        {
            key: 'sort',
            label: 'Load Order',
            sortable: true,
        },
        {
            key: 'actions',
            label: 'Actions',
            sortable: false,
        },
    ];

    getEditLink(record) {
        if (this.zoneId && this.zoneId > 0) {
            return {
                name: 'zone.dns-record.edit',
                params: { zoneId: this.zoneId, dnsRecordId: record.id },
            };
        }
        return {
            name: 'dns-record.edit',
            params: { dnsRecordId: record.id },
        };
    }

    destroyRecord(record) {
        dnsRecord.destroyRecord(record.id).then((res) => {
            bus.$emit('APP_ALERT', {
                text: 'Dns Record Destroyed',
                type: 'danger',
            });
            this.boot();
        });
    }

    loadData() {
        if (this.zoneId && this.zoneId > 0) {
            return dnsRecord
                .getDnsRecordsForZone(this.zoneId, this.query)
                .then((res) => {
                    let query = new GeneralQS();
                    query.page = res.pagination.page;
                    query.per_page = res.pagination.per_page;
                    query.sort_by = this.query.sort_by;
                    query.sort_dir = this.query.sort_dir;
                    this.query = query;
                    this.total = res.pagination.total;
                    this.items = res.dns_records;
                    this.isLoaded = true;
                    this.isLoading = false;
                });
        } else {
            return dnsRecord.getDnsRecords(this.query).then((res) => {
                let query = new GeneralQS();
                query.page = res.pagination.page;
                query.per_page = res.pagination.per_page;
                query.sort_by = this.query.sort_by;
                query.sort_dir = this.query.sort_dir;
                this.query = query;
                this.total = res.pagination.total;
                this.items = res.dns_records;
                this.isLoaded = true;
                this.isLoading = false;
            });
        }
    }
    boot() {
        this.loadData();
    }

    mounted() {
        this.query.sort_by = 'sort';
        this.boot();
        bus.$on('DNS_SERVER_ADDED', (payload) => {
            this.boot();
        });
    }
}
</script>
