<template>
    <div class="home-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row">
                <div class="col-md-6 offset-md-3 col-xs-12">
                    <zones-table></zones-table>
                </div>
            </div>
        </b-container>
    </div></template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

@Component
export default class Home extends Vue {

}
</script>
