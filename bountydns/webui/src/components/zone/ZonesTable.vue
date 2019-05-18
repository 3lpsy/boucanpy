<template id="">
    <div class="" v-if="isAuthenticated">
        <b-table
            striped
            hover
            :items="items"
            :fields="fields"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
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
                >
                    Deactivate
                </b-button>
                <b-button
                    size="sm"
                    @click="activateAction(row.item, row.index, $event.target)"
                    v-if="!row.item.is_active"
                >
                    Activate
                </b-button>
            </template>
            <template slot="edit" slot-scope="row">
                <router-link
                    :to="{ name: 'zone.edit', params: { zoneId: row.item.id } }"
                ></router-link>
            </template>
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

import zone from '@/services/zone';

// TODO: move to vuex / persistent data
@Component
export default class ZonesTable extends mixins(
    CommonMixin,
    ZoneMixin,
    DataTableMixin,
) {
    isLoading = true;
    sortBy = 'id';
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
        this.sortBy = sort.sortBy;
        this.sortDesc = sort.sortDesc;
        this.loadData();
    }

    changePage(page) {
        this.currentPage = page;
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
        return zone
            .getZones(
                this.currentPage || 1,
                this.perPage,
                this.sortBy,
                this.sortDesc ? 'desc' : 'asc',
                ['dns_server'],
            )
            .then((res) => {
                this.currentPage = res.pagination.page;
                this.perPage = res.pagination.per_page;
                this.total = res.pagination.total;
                this.items = res.zones;
                this.isLoaded = true;
                this.isLoading = false;
            })
            .catch((error) => {
                this.isLoading = false;
            });
    }

    freshLoad() {
        return this.loadData();
    }
    mounted() {
        this.freshLoad();
        this.registerOnBroadcastZoneCreated();
    }
}
</script>
