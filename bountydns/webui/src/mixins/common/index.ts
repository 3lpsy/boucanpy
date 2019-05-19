// mixin.js
import Vue from 'vue';
import Component from 'vue-class-component';
import { mixins } from 'vue-class-component';

// export interface ICommonMixin {
//     errors?: any;
//     inputs?: any;
// }

// You can declare a mixin as the same style as components.
@Component({})
export default class CommonMixin extends Vue {
    getInputState(fieldName: string) {
        if (this.errors.has(fieldName)) {
            return 'invalid';
        }
        let field = this.inputs.find({ name: fieldName });
        if (typeof field !== 'undefined' && field) {
            if (field!.flags.valid) {
                return 'valid';
            }
        }
        return null;
    }

    get isAuthenticated(): boolean {
        return this.$store.getters['auth/isAuthenticated'];
    }

    logout() {
        console.log('dispatching auth/defauthenticate');
        this.$store.dispatch('auth/deauthenticate').then(() => {
            this.$router.push({ name: 'login' });
        });
    }

    get errors() {
        return this.$validator.errors;
    }

    get inputs() {
        return this.$validator.fields; // @ts-ignore
    }
}
