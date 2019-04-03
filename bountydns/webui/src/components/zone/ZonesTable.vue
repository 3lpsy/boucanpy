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
    sortBy = 'id';
    revealed = {
        id: 0,
        token: '',
    };
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
            key: 'dns_server_name',
            label: 'Server',
        },
        {
            key: 'actions',
            label: 'Status',
        },
    ];

    changeSort(sort) {
        this.sortBy = sort.sortBy
        this.sortDesc = sort.sortDesc
        this.loadData()
    }

    changePage(page) {
        this.currentPage = page;
        this.loadData()
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
        return zone.getZones(this.currentPage || 1, this.perPage, this.sortBy, this.sortDesc ? 'desc' : 'asc')
        .then((res) => {
            this.currentPage = res.pagination.page;
            this.perPage = res.pagination.per_page;
            this.total = res.pagination.total;
            this.items = res.zones;
            this.isLoaded = true;
        });
    }

    freshLoad() {
        this.loadData()
    }
    mounted() {
        this.freshLoad();
    }
}
</script>
