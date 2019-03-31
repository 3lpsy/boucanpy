
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
    AppAlerts
  },
})
export default class App extends Vue {
}
</script>

<style lang='scss'>
@import '~@/assets/scss/main.scss';

#app {
    height: 100%;
    width: 100%;
    margin-bottom: 60px;
}
</style>
