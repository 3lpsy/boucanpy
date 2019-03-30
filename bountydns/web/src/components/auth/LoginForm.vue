<template>
    <b-form @submit="onSubmit" v-if="show">
        <fieldset class="form-group">
            <input
                type="text"
                placeholder="Email"
                class="form-control form-control-lg"
                v-model="form.username"
            >
        </fieldset>

        <fieldset class="form-group">
            <input
                type="password"
                placeholder="Password"
                class="form-control form-control-lg"
                v-model="form.password"
            >
        </fieldset>
        <ul class="error-messages" v-if="loginError">
            <li>{{ loginError }}</li>
        </ul>
        <button class="btn btn-lg btn-primary pull-xs-right">
            Sign in
        </button>
    </b-form>
</template>

<script lang="ts">
    import { Vue, Component } from 'vue-property-decorator';
    import { mixins } from 'vue-class-component';
    import CommonMixin from '@/mixins/common';
    import {LoginForm as LoginFormData} from '@/types';
    import authService from '@/services/auth';

    @Component
    export default class LoginForm extends mixins(CommonMixin) {
        show: boolean = true
        loginError: string = ''
        form: LoginFormData = {
            username: '',
            password: ''
        }
        onSubmit() {
            authService
              .login(this.form)
              .then((accessToken) => {
                  console.log("Recieved login token", accessToken);
                  this.$router.push('/')
              })
              .catch((err) => {
                console.error(err);
                this.loginError = 'Invalid username or password';
              });
        }

    }
</script>
