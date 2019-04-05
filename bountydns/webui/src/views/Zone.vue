<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row">
                <div class="col-md-9 col-xs-12">
                    <h2>Zones</h2>
                </div>
                <div class="col-md-3 col-xs-12">
                    <b-button
                        v-b-modal.create-zone
                        class="pull-right"
                        style="width:100%"
                        variant="outline-primary"
                    >
                        Create Zone
                    </b-button>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <zones-table></zones-table>
                </div>
            </div>
        </b-container>
        <zone-create-modal modal-id="create-zone"> </zone-create-modal>
    </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import ZonesTable from '@/components/zone/ZonesTable.vue';
import ZoneCreateModal from '@/components/zone/ZoneCreateModal.vue';

@Component({ components: { ZonesTable, ZoneCreateModal } })
export default class Home extends Vue {}
</script>
