<template id="">
    <div class v-if="isAuthenticated">
        <b-table
            striped
            hover
            :items="items"
            :fields="fields"
            :sort-by.sync="query.sort_by"
            :sort-desc="query.sort_dir == 'desc'"
            v-on:sort-changed="changeSort"
            :responsive="true"
            :busy="isLoading || !isLoaded"
        >
            <tempalte v-slot:table-busy class="text-center text-danger my-2">
                <b-spinner class="align-middle"></b-spinner>
                <strong>Loading...</strong>
            </tempalte>
            <!-- TODO: don't use expires_at, use expires delta -->
            <template v-slot:cell(actions)="row">
                <div>
                    <b-button
                        style="margin: 5px"
                        size="sm"
                        @click="
                        deactivateAction(row.item, row.index, $event.target)
                    "
                        v-if="row.item.is_active"
                    >Deactivate</b-button>
                    <b-button
                        style="margin: 5px"
                        size="sm"
                        @click="activateAction(row.item, row.index, $event.target)"
                        v-if="!row.item.is_active"
                    >Activate</b-button>
                    <router-link
                        style="margin: 5px"
                        :to="{ name: 'user.edit', params: { userId: row.item.id } }"
                        tag="button"
                        class="btn btn-warning btn-sm"
                    >Edit</router-link>
                    <!-- <router-link
                        :to="{ name: 'user.show', params: { userId: row.item.id } }"
                        tag="button"
                        class="btn btn-info btn-sm"
                    >View</router-link>-->
                </div>
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
import { GeneralQS } from '@/queries';

import user from '@/services/user';

// TODO: move to vuex / persistent data
@Component({})
export default class UsersTable extends mixins(CommonMixin, DataTableMixin) {
    query = new GeneralQS();
    isLoading = true;
    fields = [
        {
            key: 'id',
            label: 'ID',
            sortable: true,
        },
        {
            key: 'email',
            label: 'Email',
            sortable: true,
        },
        {
            key: 'is_superuser',
            label: 'Super',
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

    changePage(page) {
        this.query.page = page;
        this.loadData();
    }

    deactivateAction(item, index, target) {
        user.deactivateUser(item.id)
            .then((res) => {
                this.freshLoad();
            })
            .catch((e) => {
                this.handleApiError(e);
            });
    }

    activateAction(item, index, target) {
        user.activateUser(item.id)
            .then((res) => {
                this.freshLoad();
            })
            .catch((e) => {
                this.handleApiError(e);
            });
    }

    loadData() {
        this.isLoading = true;
        return user
            .getUsers(this.query)
            .then((res) => {
                let query = new GeneralQS();
                query.page = res.pagination.page;
                query.per_page = res.pagination.per_page;
                query.sort_by = this.query.sort_by;
                query.sort_dir = this.query.sort_dir;
                this.query = query;
                this.total = res.pagination.total;
                this.items = res.users;
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
        // this.registerOnBroadcastZoneCreated();
    }
}
</script>
