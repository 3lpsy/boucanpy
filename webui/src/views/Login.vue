<template>
    <div class="page auth-page row">
        <b-container style="padding-top: 10px" class="page">
            <div class="row">
                <div class="col-md-6 offset-md-3 col-xs-12">
                    <h1 class="text-center">
                        Sign in
                    </h1>
                    <p></p>
                    <login-form></login-form>
                </div>
            </div>
        </b-container>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import LoginForm from '@/components/auth/LoginForm.vue';

@Component({
    components: {
        LoginForm,
    },
})
export default class Login extends Vue {}
</script>
