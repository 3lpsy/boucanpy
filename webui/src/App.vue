<template>
    <div id="app">
        <app-navbar></app-navbar>
        <app-alerts></app-alerts>
        <router-view></router-view>
        <app-footer></app-footer>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import AppFooter from '@/components/AppFooter.vue';
import AppNavbar from '@/components/AppNavbar.vue';
import AppAlerts from '@/components/AppAlerts.vue';
import bus from '@/bus';

@Component({
    components: {
        AppFooter,
        AppNavbar,
        AppAlerts,
    },
})
export default class App extends Vue {
    created() {
        bus.$on('DNS_REQUEST_CREATED', (event: any) => {
            bus.$emit('APP_ALERT', {
                text: 'New DNS Request Added!',
                type: 'info',
            });
        });
        bus.$on('HTTP_REQUEST_CREATED', (event: any) => {
            bus.$emit('APP_ALERT', {
                text: 'New HTTP Request Added!',
                type: 'info',
            });
        });
        bus.$on('ZONE_CREATED', (event: any) => {
            bus.$emit('APP_ALERT', { text: 'New Zone Added!', type: 'info' });
        });
        bus.$on('API_TOKEN_CREATED', (event: any) => {
            bus.$emit('APP_ALERT', {
                text: 'New Api Token Created!',
                type: 'info',
            });
        });
    }
}
</script>

<style lang="scss">
@import '~@/assets/scss/main.scss';

body {
    background-color: #f5f5f5;
}
#app {
    display: block;
    height: 100%;
    width: 100%;
    background-color: #f5f5f5;
}
.page {
    background-color: #ffffff;
    padding-bottom: 20px;
}
</style>
