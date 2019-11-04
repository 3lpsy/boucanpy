<template>
    <b-form @submit.prevent="onSubmit" v-if="show">
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
        <button class="btn btn-lg btn-primary pull-xs-right">Sign in</button>
    </b-form>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
import { LoginForm as LoginFormData, User } from '@/types';
import authService from '@/services/auth';

@Component({})
export default class LoginForm extends mixins(CommonMixin) {
    show: boolean = true;
    loginError: string = '';
    form: LoginFormData = {
        username: '',
        password: '',
    };
    onSubmit() {
        console.log('dispatching auth/authenticate');
        this.$store
            .dispatch('auth/authenticate', this.form)
            .then((user: User) => {
                this.$router.push({ name: 'home' });
            })
            .catch((err) => {
                this.loginError = 'Authentication failed';
                console.log('ERROR', err);
                this.handleApiError(err);
            });
    }
}
</script>
