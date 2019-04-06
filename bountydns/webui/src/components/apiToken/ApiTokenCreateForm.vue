<template id="">
    <b-form @submit.prevent="onSubmit">
        <fieldset class="form-group">
            <label for="input-scopes">Scopes</label>
            <input
                id="input-scopes"
                type="text"
                placeholder="Scopes"
                class="form-control form-control-lg"
                v-model="form.scopes"
            />
            <small
                >Note: The 'dns-request' or 'dns-request:create' (same for
                dns-response) scopes are required for the DNS server</small
            >
        </fieldset>
        <fieldset class="form-group">
            <label for="input-exp">Expiration</label>
            <input
                id="input-exp"
                type="date"
                placeholder="Scopes"
                class="form-control form-control-lg"
                v-model="form.expires_at"
            />
        </fieldset>
        <fieldset class="form-group">
            <label for="input-server-name">DNS Server Name</label>
            <vue-bootstrap-typeahead
                :data="dnsServers"
                v-model="dnsServersSearch"
                size="lg"
                placeholder="Type a DNS Server Name"
                @hit="form.dns_server_name = $event"
                :min-matching-chars="0"
            >
            </vue-bootstrap-typeahead>
            <small>
                The DNS Server which will use the zone. If left blank, all DNS
                Servers will use the zone.
            </small>
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
import ApiTokenMixin from '@/mixins/apiToken';
import DnsServersMixin from '@/mixins/dnsServer';

import apiToken from '@/services/apiToken';
import moment from 'moment';
import bus from '@/bus';

@Component({
    watch: {
        dnsServersSearch() {
            console.log('dnsServersSearch');
            this.getDnsServers(name).then((res) => {
                this.dnsServers = res.dns_servers.map((d) => d.dns_server_name);
            });
        },
    },
})
export default class ApiTokensCreateForm extends mixins(
    CommonMixin,
    ApiTokenMixin,
    DnsServersMixin,
) {
    dnsServers = [];
    dnsServersSearch = uuid4();
    formError = '';
    form = {
        scopes:
            'profile dns-request:create dns-request:list zone:list zone:read refresh',
        expires_at: '',
        dns_server_name: '',
    };
    default_uuid = '';
    onSubmit() {
        let data = {
            scopes: this.form.scopes,
            expires_at: moment(this.form.expires_at, 'YYYY-MM-DD').unix(),
            dns_server_name: this.form.dns_server_name,
        };
        console.log('submitting data', data);
        apiToken.createApiToken(data).then(() => {
            console.log('emiting app event');
            bus.$emit('APP_ALERT', {
                text: 'Api Token Created',
                type: 'success',
            });
            bus.$emit('API_TOKEN_CREATED', data.token);
            console.log('emiting formComplete event');
            this.$emit('form-complete');
        });
    }

    mounted() {
        // this.form.scopes = this.$store.getters['auth/getToken'].scopes.join(
        //     ' ',
        // );
        this.form.expires_at = moment()
            .add(90, 'days')
            .format('YYYY-MM-DD');
    }
}
</script>
