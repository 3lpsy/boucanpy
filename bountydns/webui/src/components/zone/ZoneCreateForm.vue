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
            >
            </b-form-input>
            <template v-slot:invalid-feedback>
                {{ errors.first('domain') }}
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
            >
            </b-form-input>
            <template v-slot:invalid-feedback>
                {{ errors.first('ip') }}
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
            >
            </vue-bootstrap-typeahead>
        </b-form-group>
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
import CommonMixin from '@/mixins/common';
import ZoneMixin from '@/mixins/zone';
import DataTableMixin from '@/mixins/dataTable';
import DnsServersMixin from '@/mixins/dnsServer';
import zone from '@/services/zone';
import dnsServer from '@/services/dnsServer';
import { GeneralQS , IGeneralQS} from '@/queries';

import bus from '@/bus';

// TODO: remove underscore
import _ from 'underscore';

@Component({
    watch: {
        dnsServersSearch(value) {
            this.query.searchv = value
            dnsServer.getDnsServers(this.query).then((res) => {
                this.dnsServers = res.dns_servers
            });
        },
    },
})
export default class ZoneCreateForm extends mixins(
    CommonMixin,
    ZoneMixin,
    DnsServersMixin,
    DataTableMixin,
) {
    formError = '';
    dnsServers = [];
    dnsServersSearch = '';
    disabled = false
    query = new GeneralQS();
    form = {
        domain: '',
        ip: '',
        dns_server_id: '',
    };

    collectForm() {
        return new Promise((resolve, reject) => {
            let form = Object.keys(this.form)
              .filter(key => {
                  if (key == "dns_server_id") {
                      return this.form[key] && this.form[key] > 0;
                  }
                  else {
                      return true
                  }
              }).reduce((obj, key) => {
                  obj[key] = this.form[key];
                  return obj;
              }, {});

             resolve(form)
        })
    }

    confirmDataIfRequired() {
        return new Promise((resolve, reject) => {
            if (this.form.dns_server_id && this.form.dns_server_id > 0) {
                resolve(true)
            } else {
                this.$bvModal.msgBoxConfirm('Please confirm that you want to delete everything.', {
                      title: 'Please Confirm',
                      size: 'sm',
                      buttonSize: 'sm',
                      okVariant: 'info',
                      okTitle: 'YES',
                      cancelTitle: 'NO',
                      footerClass: 'p-2',
                      hideHeaderClose: false,
                      centered: true
                }).then((answer) => {
                    resolve(answer)
                })
            }
        })
    }

    onSubmit() {
        this.$validator.validateAll().then((valid) => {
            if (valid) {
                this.disabled = true
                console.log('submitting data', this.form);
                this.confirmDataIfRequired().then((answer) => {
                    if (answer) {
                        this.collectForm().then((form) => {
                            zone.createZone(form).then(() => {
                                bus.$emit('APP_ALERT', { text: 'Zone Created', type: 'success' });
                                this.$emit('form-complete');
                                this.form = {
                                    domain: '',
                                    ip: '',
                                    dns_server_id: '',
                                }
                                this.disabled = false
                            }).catch((error) => {
                                this.disabled = false
                                throw error;
                            });
                        })
                    } else {
                        this.disabled = false
                    }
                })

            }
       });
    }

    getInputState(fieldName) {
        if (this.errors.has(fieldName)) {
            return 'invalid'
        }
        else if (this.inputs.domain && this.inputs.domain.valid) {
            return 'valid'
        }
        return null
    }

    mounted() {
        this.query = new GeneralQS()
    }
}
</script>
