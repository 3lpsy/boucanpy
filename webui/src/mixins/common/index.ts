// mixin.js
import Vue from 'vue';
import Component from 'vue-class-component';
import { mixins } from 'vue-class-component';
import { capitalize } from '@/utils';
import { User } from '@/types';
import bus from '@/bus';
import moment from 'moment';

@Component
export default class CommonMixin extends Vue {
    getInputState(fieldName: string) {
        if (this.errors.has(fieldName)) {
            return false;
        }
        let field = this.getField(fieldName);
        if (typeof field !== 'undefined' && field) {
            if (field!.flags.valid) {
                return true;
            }
        }
        return null;
    }

    getField(fieldName: string) {
        return this.inputs.find({ name: fieldName });
    }

    get authUser(): User {
        return this.$store.getters['auth/getUser'];
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
        if (!e || !e.response) {
            console.log('No response on error');
            return;
        }

        let response = e.response;
        if (response.data) {
            let data = response.data;

            if (data.detail) {
                let detail = data.detail;
                if (Array.isArray(detail)) {
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
                        } else {
                            let message = item.loc.join('.') + ' - ' + item.msg;
                            this.handleGlobalError({
                                status: response.status,
                                message: message,
                            });
                        }
                    }
                } else if (
                    typeof detail === 'string' ||
                    detail instanceof String
                ) {
                    this.handleGlobalError({
                        status: response.status,
                        message: detail,
                    });
                }
            }
        }
    }

    handleGlobalError(error: any) {
        let code = error.status || 500;
        let status = String(code);
        let message = error.message || 'Unkown Error';
        let toastMsg = status + ': ' + message;

        bus.$emit('APP_TOAST', {
            message: toastMsg,
            options: {
                title: 'Application Message',
                variant: 'danger',
                toaster: 'b-toaster-bottom-right',
            },
        });
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

    diffForHumans(target: moment.Moment) {
        return target.fromNow();
    }

    moment(val: any) {
        return moment(val);
    }

    truncate(target: string, limit: number) {
        return target.length > limit ? target.substr(0, limit - 1) : target;
    }

    truncateWithTrail(target: string, limit: number, trail: string) {
        return target.length > limit
            ? target.substr(0, limit - 1) + trail
            : target;
    }
}
