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
                @click="deactivateAction(row.item, row.index, $event.target)"
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

        <div class="col-xs-12 text-center" v-if="items.length < 1 && ! isLoaded">
            <span class="text-center">Loading Data</span>
        </div>

        <b-pagination
            v-if="currentPage > 0 && items.length > 0"
            v-model="currentPage"
            :total-rows="itemCount"
            :per-page="perPage"
            aria-controls="my-table"
        ></b-pagination>

    </div>

</template>

<script>
import { Vue, Component } from 'vue-property-decorator';
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
import ApiTokenMixin from '@/mixins/apiToken';
import DataTableMixin from '@/mixins/dataTable';

import apiToken from '@/services/apiToken';

// TODO: move to vuex / persistent data
@Component
export default class ApiTokensTable extends mixins(CommonMixin, ApiTokenMixin, DataTableMixin) {
    fields = [
        {
            key: 'id',
            label: 'ID',
            sortable: true
        },
        {
            key: 'scopes',
            label: 'Scopes',
            sortable: true
        },
        {
            key: 'expires_at',
            label: 'Expires',
            sortable: true
        },
        {
            key: 'actions',
            label: 'Status'
        },
        {
            key: 'reveal',
            label: 'Reveal'
        }
    ]

    deactivateAction(token, index, target) {
        apiToken.deactivateApiToken(token.id).then((res) => {
            this.freshLoad()
        })
    }

    revealAction(token, index, target) {

    }

    loadData() {
        return apiToken.getApiTokens(this.currentPage, this.perPage)
    }

    freshLoad() {
        this.loadData().then((res) => {
            this.currentPage = res.pagination.page
            this.perPage = res.pagination.per_page
            this.items = res.api_tokens
            this.isLoaded = true
        })
    }
    mounted() {
        this.freshLoad()
    }
}
</script>
