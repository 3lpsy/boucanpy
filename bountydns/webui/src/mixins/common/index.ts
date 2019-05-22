// mixin.js
import Vue from 'vue';
import Component from 'vue-class-component';
import { mixins } from 'vue-class-component';
import { capitalize } from '@/utils';

@Component({})
export default class CommonMixin extends Vue {
    getInputState(fieldName: string) {
        if (this.errors.has(fieldName)) {
            return 'invalid';
        }
        let field = this.getField(fieldName);
        if (typeof field !== 'undefined' && field) {
            if (field!.flags.valid) {
                return 'valid';
            }
        }
        return null;
    }

    getField(fieldName: string) {
        return this.inputs.find({ name: fieldName });
    }

    get isAuthenticated(): boolean {
        return this.$store.getters['auth/isAuthenticated'];
    }

    logout() {
        this.$store.dispatch('auth/deauthenticate').then(() => {
            this.$router.push({ name: 'login' });
        });
    }

    get errors() {
        return this.$validator.errors;
    }

    handleApiError(e: any) {
        if (!e || !e.response) return;

        let response = e.response;
        if (response.status == 422 && response.data) {
            let data = response.data;

            if (data.detail) {
                let detail = data.detail;

                for (let item of detail) {
                    if (
                        item.loc.includes('body') &&
                        item.loc.includes('form')
                    ) {
                        let msg = item.msg;
                        let fieldName = item.loc[item.loc.length - 1];

                        if (this.getField(fieldName)) {
                            this.addError(fieldName, msg);
                        }
                    }
                }
            }
        }
    }

    addError(fieldName: string, msg: string) {
        // Do I need to worry about scope?
        const field = this.$validator.fields.find({
            name: fieldName,
        });
        if (!field) return;

        this.$validator.errors.add({
            id: field.id,
            field: fieldName,
            msg: capitalize(msg),
        });
        field.flags.invalid = true;
        field.flags.valid = false;
        field.flags.validated = true;
    }

    get inputs() {
        return this.$validator.fields; // @ts-ignore
    }
}
