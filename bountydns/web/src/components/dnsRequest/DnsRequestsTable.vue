<template id="">
    <div class="" v-if="isAuthenticated">
        <b-table
            v-if="items.length > 0"
            striped
            hover
            :items="items"
            :fields="fields"
        >
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
            :total-rows="rows"
            :per-page="perPage"
            aria-controls="my-table"
        ></b-pagination>

    </div>

</template>

<script>
import { Vue, Component } from 'vue-property-decorator';
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
import DnsRequestMixin from '@/mixins/dnsRequest';
import dnsRequest from '@/services/dnsRequest';

// TODO: move to vuex / persistent data
@Component
export default class DnsRequestsTable extends mixins(CommonMixin, DnsRequestMixin) {
    isLoaded = false
    currentPage = 0
    perPage = 20
    items = []
    fields = {
        id: {
            label: 'ID',
            sortable: true
        },
        name: {
            label: 'Name',
            sortable: true
        },
        source_address: {
            label: 'Source',
            sortable: true
        },
        type: {
            label: 'Type',
            sortable: true
        }
    }

    get rows() {
        return this.items.length
    }


    mounted() {
        dnsRequest.getDnsRequests(this.currentPage, this.perPage).then((res) => {
            this.currentPage = res.pagination.page
            this.perPage = res.pagination.per_page
            this.items = res.dns_requests
            this.isLoaded = true
        })
    }
}
</script>
