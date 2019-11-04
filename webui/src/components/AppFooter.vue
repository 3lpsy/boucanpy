<template>
    <footer class="footer row">
        <div class="container text-center">
            <a href="https://twitter.com/3lpsy" class="logo-font">@bountydns</a>
            <span class="attribution"></span>
        </div>
    </footer>
</template>

<script>
import Vue from 'vue';
import Component from 'vue-class-component';
@Component({})
export default class AppFooter extends Vue {}
</script>

<style media="screen">
.footer {
    /* position: absolute; */
    /* bottom: 0; */
    width: 100%;
    height: 60px;
    line-height: 60px;
    background-color: #f5f5f5;
    margin-top: 10px;
}
</style>
