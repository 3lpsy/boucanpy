<template id="">
    <b-form @submit.prevent="onSubmit">
        <b-form-group
            label="Email"
            label-for="input-email"
            description="The User's email address"
            :disabled="disabled"
        >
            <b-form-input
                id="input-email"
                name="email"
                type="email"
                placeholder="jim@jim.com"
                class="form-control form-control-lg"
                v-model="form.email"
                v-validate="'required|email'"
                :state="getInputState('email')"
            ></b-form-input>
            <template v-slot:invalid-feedback>
                {{
                errors.first('email')
                }}
            </template>
        </b-form-group>
        <b-form-group
            label="Password"
            label-for="input-password"
            description="The User's password"
            :disabled="disabled"
        >
            <b-form-input
                id="input-password"
                name="password"
                type="password"
                placeholder="*****"
                class="form-control form-control-lg"
                v-model="form.password"
                v-validate="validatePasswordRules"
                :state="getInputState('password')"
                ref="password"
            ></b-form-input>
            <template v-slot:invalid-feedback>
                {{
                errors.first('password')
                }}
            </template>
        </b-form-group>
        <b-form-group
            label="Confirm Password"
            label-for="input-password-confirm"
            :disabled="disabled"
        >
            <b-form-input
                id="input-password-confirm"
                name="password_confirm"
                type="password"
                placeholder="*****"
                class="form-control form-control-lg"
                v-model="form.password_confirm"
                v-validate="validatePasswordConfirmRules"
                :state="getInputState('password_confirm')"
            ></b-form-input>
            <template v-slot:invalid-feedback>
                {{
                errors.first('password_confirm')
                }}
            </template>
        </b-form-group>
        <b-form-group label-for="input-is-superuser" :disabled="disabled">
            <b-form-checkbox
                id="input-is-superuser"
                name="is_superuser"
                v-model="form.is_superuser"
                :value="true"
                :unchecked-value="false"
                v-validate="''"
            >Super User Access?</b-form-checkbox>
            <template v-slot:invalid-feedback>
                {{
                errors.first('is_superuser')
                }}
            </template>
        </b-form-group>
        <ul class="error-messages" v-if="formError">
            <li>{{ formError }}</li>
        </ul>
        <button class="btn btn-lg btn-primary pull-right">Submit</button>
    </b-form>
</template>

<script>
import Component from 'vue-class-component';
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
import DataTableMixin from '@/mixins/dataTable';
import user from '@/services/user';
import { GeneralQS } from '@/queries';

import bus from '@/bus';

// TODO: remove underscore
import _ from 'underscore';

@Component({
    props: {
        mode: {
            type: String,
            default: 'create',
        },
        userId: {
            type: Number,
            default: 0,
        },
    },
})
export default class UserForm extends mixins(CommonMixin, DataTableMixin) {
    formError = '';
    disabled = false;
    form = {
        email: '',
        password: '',
        password_confirm: '',
        is_superuser: false,
    };

    get validatePasswordConfirmRules() {
        let base = '';

        if (this.mode == 'create') {
            base = 'required|';
        }
        return 'min:8|confirmed:password';
    }

    get validatePasswordRules() {
        let base = '';

        if (this.mode == 'create') {
            base = 'required|';
        }
        return 'min:8';
    }

    collectForm() {
        return new Promise((resolve, reject) => {
            if (this.mode == 'create') {
                resolve(this.form);
            } else {
                let form = {
                    email: this.form.email,
                    is_superuser: this.form.is_superuser,
                };
                if (this.form.password && this.form.password.length > 0) {
                    form.password = this.form.password;
                    form.password_confirm = this.form.password_confirm;
                }
                resolve(form);
            }
        });
    }

    onSubmit() {
        if (!this.disabled) {
            this.$validator.validateAll().then((valid) => {
                if (valid) {
                    this.disabled = true;
                    this.collectForm().then((form) => {
                        if (this.mode == 'create') {
                            user.createUser(form)
                                .then(() => {
                                    bus.$emit('APP_ALERT', {
                                        text: 'User Created',
                                        type: 'success',
                                    });
                                    this.$emit('form-complete');
                                    this.form = {
                                        email: '',
                                        password: '',
                                        password_confirm: 0,
                                        is_superuser: false,
                                    };
                                    this.disabled = false;
                                    this.$router.push({
                                        name: 'user.index',
                                    });
                                })
                                .catch((e) => {
                                    this.disabled = false;
                                    this.handleApiError(e);
                                    throw e;
                                });
                        } else {
                            user.updateUser(this.userId, form)
                                .then(() => {
                                    bus.$emit('APP_ALERT', {
                                        text: 'User Updated',
                                        type: 'success',
                                    });
                                    this.$emit('form-complete');
                                    this.boot();
                                    // this.$router.push({
                                    //     name: 'user.index',
                                    // });
                                })
                                .catch((e) => {
                                    this.disabled = false;
                                    this.handleApiError(e);
                                    throw e;
                                });
                        }
                    });
                }
            });
        }
    }

    boot() {
        this.disabled = false;
        if (this.mode == 'create') {
            this.form = {
                email: '',
                password: '',
                password_confirm: '',
                is_superuser: false,
            };
        }

        if (this.mode === 'edit') {
            user.getUser(this.userId)
                .then((res) => {
                    this.form.email = res.user.email;
                    this.form.is_superuser = res.user.is_superuser;
                })
                .catch((e) => {
                    this.handleApiError(e);
                    console.log(e);
                    throw e;
                });
        }
    }

    mounted() {
        if (this.mode == 'edit') {
            if (this.authUser.id == this.userId) {
                this.$router.push({ name: 'profile.edit' });
            }
        }
        this.boot();
    }
}
</script>
