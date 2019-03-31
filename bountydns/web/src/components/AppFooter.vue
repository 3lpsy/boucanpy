
<template>
  <footer class="footer">
    <div class="container text-center">
      <a href="/" class="logo-font">@bountydns</a>
      <span class="attribution">

      </span>
    </div>
  </footer>
</template>

<script>
import { Vue, Component } from 'vue-property-decorator';
@Component
export default class AppFooter extends Vue {}
</script>

<style media="screen">
.footer {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 60px;
    line-height: 60px;
    background-color: #f5f5f5;
}
</style>
