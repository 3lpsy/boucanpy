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
            <template v-slot:cell(dns_server_name)="row">
                <span
                    v-if="row.item.dns_server"
                >{{ truncateWithTrail(row.item.dns_server.name, 10, '...') }}</span>
            </template>
            <template v-slot:cell(http_server_name)="row">
                <span
                    v-if="row.item.http_server"
                >{{ truncateWithTrail(row.item.http_server.name, 10, '...') }}</span>
            </template>
            <!-- TODO: don't use expires_at, use expires delta -->
            <template v-slot:cell(actions)="row">
                <b-button
                    size="sm"
                    @click="
                        deactivateAction(row.item, row.index, $event.target)
                    "
                    v-if="row.item.is_active"
                >Deactivate</b-button>
                <span v-else>Dead</span>
            </template>
            <template v-slot:cell(reveal)="row">
                <b-button
                    size="sm"
                    @click="revealAction(row.item, row.index, $event.target)"
                    v-if="row.item.is_active"
                    class="btn btn-info btn-sm"
                >Reveal</b-button>

                <span v-else>Dead</span>
            </template>
            <!-- <template v-slot:cell(edit)="row">
                <router-link
                    :to="{ name: 'api-token.edit', params: { apiTokenId: row.item.id } }"
                    tag="button"
                    class="btn btn-warning btn-sm"
                    v-if="row.item.is_active"
                >Edit</router-link>
                <span v-else>Dead</span>
            </template>-->
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

        <b-modal
            ref="token-reveal-modal"
            size="lg"
            hide-footer
            id="reveal-api-token"
            :title="'Api Token (' + revealed.id + ')'"
        >
            <div class="container">
                <p class="text-left" style="word-wrap: break-word">
                    <span>
                        <strong>DNS Server Name:</strong>
                        <br>
                        {{ revealed.dns_server_name || "None"}}
                    </span>
                    <br>
                    <span>
                        <strong>HTTP Server Name:</strong>
                        <br>
                        {{ revealed.http_server_name || "None"}}
                    </span>
                    <br>
                    <br>
                    <span>
                        <strong>Token:</strong>
                        <br>
                        {{ revealed.token }}
                    </span>
                </p>
            </div>
        </b-modal>
    </div>
</template>

<script>
import Vue from 'vue';
import Component from 'vue-class-component';
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
import DataTableMixin from '@/mixins/dataTable';
import apiToken from '@/services/apiToken';
import bus from '@/bus';
import { GeneralQS } from '@/queries';

// TODO: move to vuex / persistent data
@Component({ name: 'ApiTokensTable' })
export default class ApiTokensTable extends mixins(CommonMixin, DataTableMixin) {
    query = new GeneralQS();
    isLoading = false;
    revealed = {
        id: 0,
        token: '',
        dns_server_name: '',
    };
    fields = [
        {
            key: 'id',
            label: 'ID',
            sortable: true,
        },
        {
            key: 'scopes',
            label: 'Scopes',
            sortable: true,
        },
        {
            key: 'dns_server_name',
            label: 'DNS',
            sortable: true,
        },
        {
            key: 'http_server_name',
            label: 'HTTP',
            sortable: true,
        },
        {
            key: 'expires_at',
            label: 'Expires',
            sortable: true,
            formatter: 'formatDate',
        },
        {
            key: 'actions',
            label: 'Status',
        },
        // {
        //     key: 'edit',
        //     label: 'Edit',
        // },
        {
            key: 'reveal',
            label: 'Reveal',
        },
    ];

    deactivateAction(token, index, target) {
        apiToken.deactivateApiToken(token.id).then((res) => {
            this.freshLoad();
        });
    }

    revealAction(token, index, target) {
        apiToken.getSensitiveApiToken(token.id, ['dns_server', 'http_server']).then((res) => {
            let token = res.api_token;
            this.revealed.id = token.id;
            this.revealed.token = token.token;
            this.revealed.dns_server_name = token.dns_server ? token.dns_server.name : '';
            this.revealed.http_server_name = token.http_server ? token.http_server.name : '';

            this.openRevealedModal();
        });
    }

    openRevealedModal() {
        this.$refs['token-reveal-modal'].show();
    }

    closeRevealedModal() {
        console.log('Closing modal');
        this.$refs['token-reveal-modal'].hide();
    }

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
        this.query.includes = ['dns_server', 'http_server'];
        return apiToken
            .getApiTokens(this.query)
            .then((res) => {
                let query = new GeneralQS();
                query.page = res.pagination.page;
                query.per_page = res.pagination.per_page;
                query.sort_by = this.query.sort_by;
                query.sort_dir = this.query.sort_dir;
                this.query = query;
                this.total = res.pagination.total;
                this.items = res.api_tokens;
                this.isLoaded = true;
                this.isLoading = false;
            })
            .catch((err) => {
                this.isLoading = false;
                this.handleApiError(err);
                throw err;
            });
    }

    boot() {
        this.loadData();
    }

    mounted() {
        this.boot();
        bus.$on('API_TOKEN_ADDED', (payload) => {
            this.boot();
        });
    }
}
</script>
