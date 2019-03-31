// mixin.js
import Vue from 'vue';
import Component from 'vue-class-component';

// You can declare a mixin as the same style as components.
@Component
export default class MyMixin extends Vue {
    get isAuthenticated(): boolean {
        return this.$store.getters['auth/isAuthenticated'];
    }

    logout() {
        console.log("dispatching auth/defauthenticate")
        this.$store.dispatch('auth/deauthenticate').then(() => {
            this.$router.push({name: 'login'})
        })
    }
}
