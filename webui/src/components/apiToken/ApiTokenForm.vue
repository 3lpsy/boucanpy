<template id="">
    <b-form @submit.prevent="onSubmit">
        <b-form-group
            label="Scopes"
            label-for="input-scopes"
            description="The scopes (permissions) to provide to the API token"
            :disabled="disabled || mode === 'edit'"
        >
            <b-form-input
                id="input-scopes"
                name="scopes"
                type="text"
                placeholder="example.com"
                class="form-control form-control-lg"
                v-model="form.scopes"
                v-validate="'required'"
                :state="getInputState('scopes')"
                :disabled="disabled || mode === 'edit'"
            ></b-form-input>
            <template v-slot:invalid-feedback>{{ errors.first('scopes') }}</template>
        </b-form-group>
        <b-form-group
            label="Expiration"
            label-for="input-expires-at"
            description="The date that the token should expire."
            :disabled="disabled || mode === 'edit'"
        >
            <b-form-input
                id="input-expires-at"
                name="expires_at"
                type="date"
                class="form-control form-control-lg"
                v-model="form.expires_at"
                v-validate="'required'"
                :state="getInputState('expires_at')"
                :disabled="disabled || mode === 'edit'"
            ></b-form-input>
            <template v-slot:invalid-feedback>{{ errors.first('expires_at') }}</template>
        </b-form-group>

        <b-form-group
            label="DNS Server Name"
            label-for="input-dns-server-id"
            description="The DNS Server which will use the token."
            :disabled="disabled || mode === 'edit'"
        >
            <vue-bootstrap-typeahead
                ref="inputDnsServer"
                id="input-dns-server-id"
                name="dns_server_id"
                :data="dnsServers"
                v-model="dnsServersSearch"
                size="lg"
                placeholder="Type a DNS Server Name or ID"
                @hit="form.dns_server_id = $event.id"
                :min-matching-chars="0"
                :serializer="(item) => item.id.toString() + ': ' + item.name"
                :disabled="disabled || mode === 'edit'"
                v-validate="'required|min:1'"
                :inputClass="'is-' + getInputState('dns_server_id')"
            ></vue-bootstrap-typeahead>
            <b-form-invalid-feedback
                style="display: block;"
                v-if="errors.has('dns_server_id')"
                aria-live="assertive"
                role="alert"
            >{{ errors.first('dns_server_id') }}</b-form-invalid-feedback>
        </b-form-group>
        <b-form-group
            label="HTTP Server Name"
            label-for="input-http-server-id"
            description="The HTTP Server which will use the token."
            :disabled="disabled || mode === 'edit'"
        >
            <vue-bootstrap-typeahead
                ref="httpDnsServer"
                id="input-http-server-id"
                name="http_server_id"
                :data="httpServers"
                v-model="httpServersSearch"
                size="lg"
                placeholder="Type a HTTP Server Name or ID"
                @hit="form.http_server_id = $event.id"
                :min-matching-chars="0"
                :serializer="(item) => item.id.toString() + ': ' + item.name"
                :disabled="disabled || mode === 'edit'"
                v-validate="'required|min:1'"
                :inputClass="'is-' + getInputState('http_server_id')"
            ></vue-bootstrap-typeahead>
            <b-form-invalid-feedback
                style="display: block;"
                v-if="errors.has('http_server_id')"
                aria-live="assertive"
                role="alert"
            >{{ errors.first('http_server_id') }}</b-form-invalid-feedback>
        </b-form-group>

        <ul class="error-messages" v-if="formError">
            <li>{{ formError }}</li>
        </ul>
        <button
            class="btn btn-lg btn-primary pull-right"
            :disabled="disabled || mode === 'edit'"
        >Submit</button>
    </b-form>
</template>

<script>
import Component from 'vue-class-component';
import { mixins } from 'vue-class-component';

import CommonMixin from '@/mixins/common';

import apiToken from '@/services/apiToken';
import dnsServer from '@/services/dnsServer';
import httpServer from '@/services/httpServer';

import moment from 'moment';
import bus from '@/bus';
import { GeneralQS } from '@/queries';

@Component({
    watch: {
        dnsServersSearch(value) {
            if (value.length < 1) {
                this.form.dns_server_id = 0;
            }
            this.dnsSearchQuery.search = value;
            dnsServer.getDnsServers(this.dnsSearchQuery).then((res) => {
                this.dnsServers = res.dns_servers;
            });
        },
        httpServersSearch(value) {
            if (value.length < 1) {
                this.form.http_server_id = 0;
            }
            this.httpSearchQuery.search = value;
            httpServer.getHttpServers(this.httpSearchQuery).then((res) => {
                this.httpServers = res.http_servers;
            });
        },
    },
    props: {
        mode: {
            type: String,
            default: 'create',
        },
        apiTokenId: {
            type: Number,
            default: 0,
        },
    },
})
export default class ApiTokenForm extends mixins(CommonMixin) {
    formError = '';
    dnsServers = [];
    dnsServersSearch = '';
    dnsSearchQuery = new GeneralQS();
    httpServers = [];
    httpServersSearch = '';
    httpSearchQuery = new GeneralQS();
    disabled = false;

    form = {
        scopes:
            'profile dns-request:create dns-request:list http-request:create http-request:list zone:list zone:read refresh',
        expires_at: '',
        dns_server_id: '',
        http_server_id: '',
    };

    collectData() {
        return new Promise((resolve, reject) => {
            let data = {
                scopes: this.form.scopes,
                expires_at: moment(this.form.expires_at, 'YYYY-MM-DD').unix(),
                dns_server_id: this.form.dns_server_id,
                http_server_id: this.form.http_server_id,
            };
            resolve(data);
        });
    }
    onSubmit() {
        if (!this.disabled) {
            this.disabled = true;
            this.$validator.validateAll().then((valid) => {
                if (valid) {
                    this.collectData()
                        .then((data) => {
                            if (this.mode == 'create') {
                                apiToken
                                    .createApiToken(data)
                                    .then(() => {
                                        this.disabled = false;
                                        bus.$emit('APP_ALERT', {
                                            text: 'Api Token Created',
                                            type: 'success',
                                        });
                                        bus.$emit('API_TOKEN_CREATED');
                                        this.$router.push({
                                            name: 'api-token',
                                        });
                                    })
                                    .catch((e) => {
                                        this.disabled = false;
                                        throw e;
                                    });
                            } else {
                                apiToken
                                    .updateApiToken(data)
                                    .then(() => {
                                        this.disabled = false;
                                        bus.$emit('APP_ALERT', {
                                            text: 'Api Token updated',
                                            type: 'success',
                                        });
                                        bus.$emit('API_TOKEN_UPDATED');
                                        this.$router.push({
                                            name: 'api-token',
                                        });
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
                } else {
                    this.disabled = false;
                }
            });
        }
    }

    boot() {
        this.dnsSearchQuery = new GeneralQS();
        this.disabled = false;
        this.form = {
            scopes:
                'profile dns-request:create dns-request:list http-request:create http-request:list zone:list zone:read refresh',
            expires_at: moment()
                .add(90, 'days')
                .format('YYYY-MM-DD'),
            dns_server_id: '',
            http_server_id: '',
        };

        if (this.mode === 'edit') {
            apiToken
                .getApiToken(this.apiTokenId, ['dns_server', 'http_server'])
                .then((res) => {
                    this.form.scopes = res.api_token.scopes;
                    this.form.expires_at = moment(res.api_token.expires_at).format('YYYY-MM-DD');

                    this.form.dns_server_id = res.api_token.dns_server_id || 0;
                    let dnsStr = res.api_token.dns_server.id.toString() + ': ' + res.api_token.dns_server.name;
                    this.dnsServersSearch = dnsStr;
                    this.$refs.inputDnsServer.inputValue = dnsStr;

                    this.form.http_server_id = res.api_token.http_server_id || 0;
                    let httpStr = res.api_token.http_server.id.toString() + ': ' + res.api_token.http_server.name;
                    this.httpServersSearch = httpStr;
                    this.$refs.inputHttpServer.inputValue = httpStr;
                })
                .catch((e) => {
                    console.log(e);
                    throw e;
                });
        }
    }

    mounted() {
        this.boot();
    }
}
</script>
