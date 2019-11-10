<template id="">
    <b-form @submit.prevent="onSubmit">
        <b-form-group
            label="Zone Domain"
            label-for="input-domain"
            description="The DNS Server will create multiple rules based off the domain.
            Non Zone requests will still be logged"
            :disabled="disabled"
        >
            <b-form-input
                id="input-domain"
                name="domain"
                type="text"
                placeholder="example.com"
                class="form-control form-control-lg"
                v-model="form.domain"
                v-validate="'required|ip_or_fqdn'"
                :state="getInputState('domain')"
            ></b-form-input>
            <template v-slot:invalid-feedback>
                {{
                errors.first('domain')
                }}
            </template>
        </b-form-group>
        <b-form-group
            label="Resolve IP"
            label-for="input-ip"
            description="The IP to Answer with for Relevant DNS Requests."
            :disabled="disabled"
        >
            <b-form-input
                id="input-ip"
                name="ip"
                type="text"
                placeholder="1.2.3.4"
                class="form-control form-control-lg"
                v-model="form.ip"
                v-validate="'required|ip'"
                :state="getInputState('ip')"
            ></b-form-input>
            <template v-slot:invalid-feedback>
                {{
                errors.first('ip')
                }}
            </template>
        </b-form-group>
        <b-form-group
            label="DNS Server Name"
            label-for="input-dns-server-id"
            description="The DNS Server which will use the zone. If left blank, all DNS
            Servers will use the zone."
            :disabled="disabled"
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
                :disabled="disabled"
            ></vue-bootstrap-typeahead>
        </b-form-group>
        <b-form-group
            label="HTTP Server Name"
            label-for="input-http-server-id"
            description="The HTTP Server which will use the zone. If left blank, all HTTP
            Servers will use the zone."
            :disabled="disabled"
        >
            <vue-bootstrap-typeahead
                ref="inputHttpServer"
                id="input-http-server-id"
                name="http_server_id"
                :data="httpServers"
                v-model="httpServersSearch"
                size="lg"
                placeholder="Type a HTTP Server Name or ID"
                @hit="form.http_server_id = $event.id"
                :min-matching-chars="0"
                :serializer="(item) => item.id.toString() + ': ' + item.name"
                :disabled="disabled"
            ></vue-bootstrap-typeahead>
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
import ZoneMixin from '@/mixins/zone';
import DataTableMixin from '@/mixins/dataTable';
import zone from '@/services/zone';
import dnsServer from '@/services/dnsServer';
import httpServer from '@/services/httpServer';

import { GeneralQS } from '@/queries';

import bus from '@/bus';

// TODO: remove underscore
import _ from 'underscore';

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
        zoneId: {
            type: Number,
            default: 0,
        },
    },
})
export default class ZoneForm extends mixins(CommonMixin, ZoneMixin, DataTableMixin) {
    formError = '';
    dnsServers = [];
    dnsServersSearch = '';
    dnsSearchQuery = new GeneralQS();

    httpServers = [];
    httpServersSearch = '';
    httpSearchQuery = new GeneralQS();

    disabled = false;
    form = {
        domain: '',
        ip: '',
        dns_server_id: '',
        http_server_id: '',
    };

    collectForm() {
        return new Promise((resolve, reject) => {
            resolve(this.form);
        });
    }

    confirmDataIfRequired() {
        return new Promise((resolve, reject) => {
            if (this.form.dns_server_id && this.form.dns_server_id > 0) {
                resolve(true);
            } else {
                this.$bvModal
                    .msgBoxConfirm(
                        'Please confirm that you want to create a global zone that will be made available to all DNS Servers.',
                        {
                            title: 'Please Confirm',
                            size: 'sm',
                            buttonSize: 'sm',
                            okVariant: 'info',
                            okTitle: 'YES',
                            cancelTitle: 'NO',
                            footerClass: 'p-2',
                            hideHeaderClose: false,
                            centered: true,
                        },
                    )
                    .then((answer) => {
                        resolve(answer);
                    });
            }
        });
    }

    onSubmit() {
        if (!this.disabled) {
            this.$validator.validateAll().then((valid) => {
                if (valid) {
                    this.disabled = true;
                    console.log('submitting data', this.form);
                    this.confirmDataIfRequired()
                        .then((answer) => {
                            if (answer) {
                                this.collectForm().then((form) => {
                                    if (this.mode === 'edit') {
                                        zone.updateZone(this.zoneId, form)
                                            .then(() => {
                                                bus.$emit('APP_ALERT', {
                                                    text: 'Zone Updated',
                                                    type: 'success',
                                                });
                                                this.$emit('form-complete');
                                                this.form = {
                                                    domain: '',
                                                    ip: '',
                                                    dns_server_id: '',
                                                    http_server_id: '',
                                                };
                                                this.disabled = false;
                                                this.$router.push({
                                                    name: 'zone',
                                                });
                                            })
                                            .catch((e) => {
                                                this.disabled = false;
                                                this.handleApiError(e);

                                                throw e;
                                            });
                                    } else {
                                        zone.createZone(form)
                                            .then(() => {
                                                bus.$emit('APP_ALERT', {
                                                    text: 'Zone Created',
                                                    type: 'success',
                                                });
                                                this.$emit('form-complete');
                                                this.form = {
                                                    domain: '',
                                                    ip: '',
                                                    dns_server_id: '',
                                                    http_server_id: '',
                                                };
                                                this.disabled = false;
                                                this.$router.push({
                                                    name: 'zone',
                                                });
                                            })
                                            .catch((e) => {
                                                this.disabled = false;
                                                this.handleApiError(e);

                                                throw e;
                                            });
                                    }
                                });
                            } else {
                                this.disabled = false;
                            }
                        })
                        .catch((error) => {
                            this.disabled = false;
                            throw error;
                        });
                }
            });
        }
    }

    boot() {
        this.dnsSearchQuery = new GeneralQS();
        this.httpSearchQuery = new GeneralQS();

        this.disabled = false;
        this.form = {
            domain: '',
            ip: '',
            dns_server_id: 0,
            http_server_id: 0,
        };

        if (this.mode === 'edit') {
            zone.getZone(this.zoneId, ['dns_server', 'http_server'])
                .then((res) => {
                    this.form.ip = res.zone.ip;
                    this.form.domain = res.zone.domain;
                    this.form.dns_server_id = res.zone.dns_server_id || 0;
                    this.form.http_server_id = res.zone.http_server_id || 0;

                    if (res.zone.dns_server) {
                        let dnsStr = res.zone.dns_server.id.toString() + ': ' + res.zone.dns_server.name;
                        this.dnsServersSearch = dnsStr;
                        this.$refs.inputDnsServer.inputValue = dnsStr;
                    }
                    if (res.zone.http_server) {
                        let httpStr = res.zone.http_server.id.toString() + ': ' + res.zone.http_server.name;
                        this.httpServersSearch = httpStr;
                        this.$refs.inputHttpServer.inputValue = httpStr;
                    }
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
