<template>
    <div id="app">
        <app-navbar></app-navbar>
        <app-alerts></app-alerts>
        <router-view></router-view>
        <app-footer></app-footer>
    </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import AppFooter from '@/components/AppFooter.vue';
import AppNavbar from '@/components/AppNavbar.vue';
import AppAlerts from '@/components/AppAlerts.vue';

@Component({
    components: {
        AppFooter,
        AppNavbar,
        AppAlerts,
    },
})
export default class App extends Vue {
    mounted() {

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
