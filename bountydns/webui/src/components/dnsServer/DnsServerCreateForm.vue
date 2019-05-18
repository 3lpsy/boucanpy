<template id="">
    <b-form @submit.prevent="onSubmit">
        <fieldset class="form-group">
            <label for="input-name">Name</label>
            <input
                id="input-name"
                type="text"
                placeholder="Scopes"
                class="form-control form-control-lg"
                v-model="form.name"
            />
        </fieldset>
        <ul class="error-messages" v-if="formError">
            <li>{{ formError }}</li>
        </ul>
        <button class="btn btn-lg btn-primary pull-right">
            Submit
        </button>
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

@Component()
export default class DnsServerCreateForm extends mixins(
    CommonMixin,
    DnsServerMixin,
) {
    formError = '';
    form = {
        name: '',
    };
    onSubmit() {
        let data = {
            name: this.form.name,
        };
        dnsServer.createDnsServer(data).then(() => {
            console.log('emiting app event');
            bus.$emit('APP_ALERT', {
                text: 'Dns Server Created',
                type: 'success',
            });
            bus.$emit('DNS_SERVER_CREATED', data.token);
            this.$emit('form-complete');
        });
    }

    mounted() {

    }
}
</script>
