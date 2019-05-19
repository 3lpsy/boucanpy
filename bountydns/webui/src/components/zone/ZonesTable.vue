<template id="">
    <div class v-if="isAuthenticated">
        <b-table
            striped
            hover
            :items="items"
            :fields="fields"
            :sort-by.sync="query.sort_by"
            :sort-desc.sync="query.sort_dir == 'desc'"
            v-on:sort-changed="changeSort"
            :responsive="true"
            :busy="isLoading || !isLoaded"
        >
            <div slot="table-busy" class="text-center text-danger my-2">
                <b-spinner class="align-middle"></b-spinner>
                <strong>Loading...</strong>
            </div>
            <!-- TODO: don't use expires_at, use expires delta -->
            <template slot="actions" slot-scope="row">
                <b-button
                    size="sm"
                    @click="
                        deactivateAction(row.item, row.index, $event.target)
                    "
                    v-if="row.item.is_active"
                >Deactivate</b-button>
                <b-button
                    size="sm"
                    @click="activateAction(row.item, row.index, $event.target)"
                    v-if="!row.item.is_active"
                >Activate</b-button>
            </template>
            <template slot="edit" slot-scope="row">
                <router-link
                    :to="{ name: 'zone.edit', params: { zoneId: row.item.id } }"
                    tag="button"
                    class="btn btn-info btn-sm"
                >Edit</router-link>
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
import { Vue, Component } from 'vue-property-decorator';
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
import ZoneMixin from '@/mixins/zone';
import DataTableMixin from '@/mixins/dataTable';
import { GeneralQS } from '@/queries';

import zone from '@/services/zone';

// TODO: move to vuex / persistent data
@Component
export default class ZonesTable extends mixins(
    CommonMixin,
    ZoneMixin,
    DataTableMixin,
) {
    query = new GeneralQS();
    isLoading = true;
    revealed = {
        id: 0,
        token: '',
    };
    editZone = {};
    editZoneId = 0;
    fields = [
        {
            key: 'id',
            label: 'ID',
            sortable: true,
        },
        {
            key: 'domain',
            label: 'Domain',
            sortable: true,
        },
        {
            key: 'ip',
            label: 'Resolves',
            sortable: true,
        },
        {
            key: 'dns_server.name',
            label: 'Server',
        },
        {
            key: 'actions',
            label: 'Status',
        },
        {
            key: 'edit',
            label: 'Edit',
        },
    ];

    changeSort(sort) {
        console.log('change sort', sort, this.query);
        this.query.sort_by = sort.sortBy;
        if (sort.sortDesc) {
            this.query.sort_dir = 'desc';
        } else {
            this.query.sort_dir = 'asc';
        }
        this.loadData();
    }

    changePage(page) {
        this.query.page = page;
        this.loadData();
    }

    deactivateAction(token, index, target) {
        zone.deactivateZone(token.id).then((res) => {
            this.freshLoad();
        });
    }

    activateAction(token, index, target) {
        zone.activateZone(token.id).then((res) => {
            this.freshLoad();
        });
    }

    loadData() {
        this.isLoading = true;
        this.query.includes = 'dns_server';
        return zone
            .getZones(this.query)
            .then((res) => {
                let query = new GeneralQS();
                query.page = res.pagination.page;
                query.per_page = res.pagination.per_page;
                query.sort_by = this.query.sort_by;
                query.sort_dir = this.query.sort_dir;
                this.query = query;
                this.total = res.pagination.total;
                this.items = res.zones;
                this.isLoaded = true;
                this.isLoading = false;
            })
            .catch((error) => {
                this.isLoading = false;
                throw error;
            });
    }

    freshLoad() {
        return this.loadData();
    }
    mounted() {
        this.query = new GeneralQS();

        this.freshLoad();
        this.registerOnBroadcastZoneCreated();
    }
}
</script>
