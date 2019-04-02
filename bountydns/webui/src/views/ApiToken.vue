<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <h2>Api Tokens</h2>
                </div>
            </div>
            <div class="row" style="padding-bottom: 20px">
                <div class="col-md-12 col-xs-12">
                    <b-button
                        v-b-modal.create-api-token
                        class="pull-right"
                        variant="outline-primary"
                    >
                        Create Api Token
                    </b-button>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <api-tokens-table></api-tokens-table>
                </div>
            </div>
        </b-container>
        <api-token-create-modal modal-id="create-api-token">
        </api-token-create-modal>
    </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import ApiTokensTable from '@/components/apiToken/ApiTokensTable.vue';
import ApiTokenCreateModal from '@/components/apiToken/ApiTokenCreateModal.vue';

@Component({ components: { ApiTokensTable, ApiTokenCreateModal } })
export default class Home extends Vue {}
</script>
