<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-9 col-xs-12">
                    <h2 v-if="zoneId">Edit Zone: {{ zoneId }}</h2>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12 col-xs-12" v-if="zoneId && zoneId > 0">
                    <zone-form mode="edit" :zone-id="zoneId"></zone-form>
                </div>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import ZoneForm from '@/components/zone/ZoneForm.vue';

import Vue from 'vue';
import Component from 'vue-class-component';

@Component({ components: { ZoneForm } })
export default class ZoneEdit extends Vue {
    isLoading = true;
    isLoaded = false;

    get zoneId() {
        if (!this.$route.params || !this.$route.params.zoneId) {
            return 0;
        }
        try {
            return parseInt(this.$route.params.zoneId);
        } catch (e) {
            return 0;
        }
    }

    mounted() {
        if (!this.zoneId) {
            this.$router.push({ name: 'home' });
        }
        this.isLoaded = true;
    }
}
</script>
