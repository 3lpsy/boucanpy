
<template>
  <div id="app">
      <app-navbar></app-navbar>
      <router-view></router-view>
      <app-footer></app-footer>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import AppFooter from '@/components/AppFooter.vue';
import AppNavbar from '@/components/AppNavbar.vue';

@Component({
  components: {
    AppFooter,
    AppNavbar,
  },
})
export default class App extends Vue {}
</script>

<style lang='scss'>
@import '~@/assets/scss/main.scss';
</style>
