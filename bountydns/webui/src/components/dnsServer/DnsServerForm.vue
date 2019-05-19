<template id="">
    <b-form @submit.prevent="onSubmit" v-if="isLoaded">
        <b-form-group
            label="Name"
            label-for="input-name"
            description="The DNS Server name"
            :disabled="disabled"
        >
            <b-form-input
                id="input-name"
                name="name"
                type="text"
                placeholder="example.com"
                class="form-control form-control-lg"
                v-model="form.name"
                v-validate="'required|alpha_dash|min:6|max:254'"
                :state="getInputState('name')"
            ></b-form-input>
            <template v-slot:invalid-feedback>{{ errors.first('name') }}</template>
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
import uuid4 from 'uuid4';

import CommonMixin from '@/mixins/common';
import DnsServerMixin from '@/mixins/dnsServer';

import dnsServer from '@/services/dnsServer';
import moment from 'moment';
import bus from '@/bus';

@Component({
    props: {
        mode: {
            type: String,
            default: 'create',
        },
        dnsServerId: {
            type: Number,
            default: 0,
        },
    },
})
export default class DnsServerCreateForm extends mixins(
    CommonMixin,
    DnsServerMixin,
) {
    formError = '';
    form = {
        name: '',
    };
    disabled = false;
    isLoading = false;
    isLoaded = true;

    collectForm() {
        return new Promise((resolve, reject) => {
            console.log('collecting form');
            resolve(this.form);
        });
    }

    // TODO: check if not disabled before submitting
    onSubmit() {
        this.$validator.validateAll().then((valid) => {
            if (valid) {
                this.disabled = true;
                this.collectForm()
                    .then((data) => {
                        console.log('SUbmitting data');
                        if (this.mode === 'edit') {
                            dnsServer
                                .updateDnsServer(this.dnsServerId, data)
                                .then(() => {
                                    console.log('emiting app event');
                                    bus.$emit('APP_ALERT', {
                                        text: 'Dns Server Created',
                                        type: 'success',
                                    });
                                    bus.$emit('DNS_SERVER_UPDATED');
                                    this.disabled = false;
                                    this.$router.push({ name: 'server' });
                                })
                                .catch((e) => {
                                    this.disabled = false;
                                    throw e;
                                });
                        } else {
                            dnsServer
                                .createDnsServer(data)
                                .then(() => {
                                    console.log('emiting app event');
                                    bus.$emit('APP_ALERT', {
                                        text: 'Dns Server Created',
                                        type: 'success',
                                    });
                                    bus.$emit('DNS_SERVER_CREATED');
                                    this.disabled = false;
                                    this.$router.push({ name: 'server' });
                                })
                                .catch((e) => {
                                    this.disabled = false;
                                    throw e;
                                });
                        }
                    })
                    .catch((e) => {
                        this.disabled = false;
                        throw e;
                    });
            }
        });
    }

    boot() {
        this.disabled = false;
        this.form = {
            name: '',
        };

        if (this.mode === 'edit') {
            // check to make sure dnsServer exists for edit form and load data
            dnsServer
                .getDnsServer(this.dnsServerId)
                .then((res) => {
                    this.isLoaded = true;
                    this.form.name = res.dns_server.name;
                })
                .catch((e) => {
                    console.log(e);
                    throw e;
                });
        } else {
            this.isLoaded = true;
        }
    }

    mounted() {
        this.boot();
    }
}
</script>
