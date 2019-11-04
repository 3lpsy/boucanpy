<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-12 col-xs-12">
                    <h2>Create Zone</h2>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <zone-form mode="create"></zone-form>
                </div>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import ZoneForm from '@/components/zone/ZoneForm.vue';

@Component({ components: { ZoneForm } })
export default class ZoneCreate extends Vue {}
</script>
