<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-9 col-xs-12">
                    <h2 v-if="userId">Edit User: {{ userId }}</h2>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12 col-xs-12" v-if="userId && userId > 0">
                    <user-form mode="edit" :user-id="userId"></user-form>
                </div>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';

import UserForm from '@/components/user/UserForm.vue';

@Component({ components: { UserForm } })
export default class UserEdit extends mixins(CommonMixin) {
    isLoading = true;
    isLoaded = false;

    get userId() {
        if (!this.$route.params || !this.$route.params.userId) {
            return 0;
        }
        try {
            return parseInt(this.$route.params.userId);
        } catch (e) {
            return 0;
        }
    }

    mounted() {
        if (!this.userId) {
            this.$router.push({ name: 'home' });
        }
        if (this.authUser.id == this.userId) {
            this.$router.push({ name: 'profile.edit' });
        }
        this.isLoaded = true;
    }
}
</script>
