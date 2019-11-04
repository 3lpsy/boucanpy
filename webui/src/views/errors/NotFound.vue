<template>
    <div class="error-page">
        <b-container style="padding-top: 10px" class="page">
            <div class="row">
                <div class="col-md-6 offset-md-3 col-xs-12">404</div>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';

@Component({})
export default class NotFound extends Vue {}
</script>
