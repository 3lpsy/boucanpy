<template>
    <div class="page home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row" style="margin-bottom: 10px;">
                <div class="col-md-9 col-xs-12">
                    <h2>Users</h2>
                </div>
                <div class="col-md-3 col-xs-12">
                    <router-link
                        tag="button"
                        class="btn pull-right btn-outline-primary"
                        :to="{name: 'user.create'}"
                    >Create User</router-link>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12 col-xs-12">
                    <users-table></users-table>
                </div>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import UsersTable from '@/components/user/UsersTable.vue';

@Component({ components: { UsersTable } })
export default class UserIndex extends Vue {}
</script>
