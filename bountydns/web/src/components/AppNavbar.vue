<template>
        <b-navbar toggleable="lg" type="dark" variant="dark">
            <b-navbar-brand :to="{name: 'home'}">
                BountyDNS
            </b-navbar-brand>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
            <b-collapse id="nav-collapse" is-nav >
                <b-navbar-nav class="ml-auto">
                    <b-nav-item v-if="isAuthenticated" :to="{name: 'home'}">Dashboard</b-nav-item>
                    <b-nav-item v-if="! isAuthenticated":to="{name: 'login'}">Login</b-nav-item>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
</template>

<script>
import { Vue, Component } from 'vue-property-decorator';
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
@Component
export default class AppNavbar extends mixins(CommonMixin) {

}
</script>
