<template id="">
    <div class="" v-if="isAuthenticated">
        <b-table
            v-if="items.length > 0"
            striped
            hover
            :items="items"
            :fields="fields"
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
                <span v-else>
                    Dead
                </span>
            </template>
            <template slot="reveal" slot-scope="row">
                <b-button
                    size="sm"
                    @click="revealAction(row.item, row.index, $event.target)"
                    v-if="row.item.is_active"
                >
                    Reveal
                </b-button>

                <span v-else>
                    Dead
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
            v-if="currentPage > 0 && items.length > 0"
            v-model="currentPage"
            :total-rows="itemCount"
            :per-page="perPage"
            aria-controls="my-table"
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
                        <strong>Server Name (ID):</strong><br />
                        {{ revealed.dns_server_name }}
                    </span>
                    <br /><br />
                    <span>
                        <strong>Token:</strong><br />

                        {{ revealed.token }}
                    </span>
                </p>
            </div>
        </b-modal>
    </div>
</template>

<script>
import { Vue, Component } from 'vue-property-decorator';
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
import ApiTokenMixin from '@/mixins/apiToken';
import DataTableMixin from '@/mixins/dataTable';
import apiToken from '@/services/apiToken';
import bus from '@/bus';

// TODO: move to vuex / persistent data
@Component
export default class ApiTokensTable extends mixins(
    CommonMixin,
    ApiTokenMixin,
    DataTableMixin,
) {
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
            label: 'Server',
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
        apiToken.getSensitiveApiToken(token.id).then((res) => {
            let token = res.api_token;
            this.revealed.id = token.id;
            this.revealed.token = token.token;
            this.revealed.dns_server_name = token.dns_server_name;
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

    loadData() {
        return apiToken.getApiTokens(this.currentPage, this.perPage);
    }

    freshLoad() {
        this.loadData().then((res) => {
            this.currentPage = res.pagination.page;
            this.perPage = res.pagination.per_page;
            this.items = res.api_tokens;
            this.isLoaded = true;
        });
    }
    mounted() {
        this.freshLoad();
        bus.$on('API_TOKEN_ADDED', (payload) => {
            this.freshLoad();
        });
    }
}
</script>
