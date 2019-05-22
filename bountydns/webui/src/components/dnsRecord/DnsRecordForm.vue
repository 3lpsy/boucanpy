<template id="">
    <b-form @submit.prevent="onSubmit" v-if="isLoaded">
        <b-form-group
            label="Record"
            label-for="input-record"
            description="The DNS Record"
            :disabled="disabled"
        >
            <b-form-input
                id="input-record"
                name="record"
                type="text"
                placeholder="abc.com IN A 1.2.3.4"
                class="form-control form-control-lg"
                v-model="form.record"
                v-validate="'required|min:5|max:1024'"
                :state="getInputState('record')"
                :disabled="disabled"
            ></b-form-input>
            <template v-slot:invalid-feedback>{{ errors.first('record') }}</template>
        </b-form-group>
        <b-form-group
            label="Load Order"
            label-for="input-sort"
            description="The DNS Record's Load Order"
            :disabled="disabled"
        >
            <b-form-input
                id="input-sort"
                name="sort"
                type="text"
                placeholder
                class="form-control form-control-lg"
                v-model="form.sort"
                v-validate="'required|numeric'"
                :state="getInputState('sort')"
                :disabled="disabled"
            ></b-form-input>
            <template v-slot:invalid-feedback>{{ errors.first('sort') }}</template>
        </b-form-group>
        <b-form-group
            label="Load Order"
            label-for="input-sort"
            description="The DNS Record's Load Order"
            :disabled="disabled"
            v-if="! zoneId || zoneId < 0"
        >
            <!-- <b-form-input
                id="input-zone-id"
                name="sort"
                type="number"
                placeholder
                class="form-control form-control-lg"
                v-model="form.sort"
                v-validate="'required'"
                :state="getInputState('sort')"
                :disabled="disabled"
            ></b-form-input>
            <template v-slot:invalid-feedback>{{ errors.first('zone_id') }}</template>-->
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
import moment from 'moment';
import bus from '@/bus';
import dnsRecord from '@/services/dnsRecord';
@Component({
    props: {
        mode: {
            type: String,
            default: 'create',
        },
        zoneId: {
            type: Number,
            default: 0,
        },
        dnsRecordId: {
            type: Number,
            default: 0,
        },
    },
})
export default class DnsRecordForm extends mixins(CommonMixin) {
    formError = '';
    form = {
        zone_id: 0,
        record: '',
        sort: null,
    };
    disabled = false;
    isLoading = false;
    isLoaded = true;

    collectForm() {
        return new Promise((resolve, reject) => {
            let data = this.form;
            data.sort = parseInt(data.sort);
            resolve(data);
        });
    }

    onSubmit() {
        if (!this.disabled) {
            this.disabled = true;
            this.$validator.validateAll().then((valid) => {
                if (valid) {
                    this.collectForm()
                        .then((data) => {
                            if (this.mode === 'edit') {
                                if (this.zoneId && this.zoneId > 0) {
                                    dnsRecord
                                        .updateDnsRecordForZone(
                                            this.dnsRecordId,
                                            this.zoneId,
                                            data,
                                        )
                                        .then(() => {
                                            bus.$emit('APP_ALERT', {
                                                text: 'Dns Record Updated',
                                                type: 'success',
                                            });
                                            this.disabled = false;
                                            this.$router.push({
                                                name: 'zone.show',
                                                params: { zoneId: this.zoneId },
                                            });
                                        })
                                        .catch((e) => {
                                            this.handleApiError(e);
                                            this.disabled = false;
                                            throw e;
                                        });
                                } else {
                                    dnsRecord
                                        .updateDnsRecord(this.dnsRecordId, data)
                                        .then(() => {
                                            bus.$emit('APP_ALERT', {
                                                text: 'Dns Record Updated',
                                                type: 'success',
                                            });
                                            this.disabled = false;
                                            this.$router.push({
                                                name: 'home',
                                            });
                                        })
                                        .catch((e) => {
                                            this.handleApiError(e);
                                            this.disabled = false;
                                            throw e;
                                        });
                                }
                            } else {
                                if (this.zoneId && this.zoneId > 0) {
                                    dnsRecord
                                        .createDnsRecordForZone(
                                            this.zoneId,
                                            data,
                                        )
                                        .then(() => {
                                            bus.$emit('APP_ALERT', {
                                                text: 'Dns Record Created',
                                                type: 'success',
                                            });
                                            this.disabled = false;
                                            this.$router.push({
                                                name: 'zone.show',
                                                params: { zoneId: this.zoneId },
                                            });
                                        })
                                        .catch((e) => {
                                            this.handleApiError(e);
                                            this.disabled = false;
                                            throw e;
                                        });
                                } else {
                                    dnsRecord
                                        .createDnsRecord(data)
                                        .then(() => {
                                            bus.$emit('APP_ALERT', {
                                                text: 'Dns Record Created',
                                                type: 'success',
                                            });
                                            this.disabled = false;
                                            this.$router.push({
                                                name: 'zone.show',
                                                params: { zoneId: this.zoneId },
                                            });
                                        })
                                        .catch((e) => {
                                            this.handleApiError(e);
                                            this.disabled = false;
                                            throw e;
                                        });
                                }
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
        this.disabled = false;
        this.form = {
            zone_id: 0,
            record: '',
            sort: null,
        };

        if (this.mode === 'edit') {
            // check to make sure dnsServer exists for edit form and load data
            if (this.zoneId && this.zoneId > 0) {
                dnsRecord
                    .getDnsRecordForZone(this.dnsRecordId, this.zoneId)
                    .then((res) => {
                        this.isLoaded = true;
                        this.form.record = res.dns_record.record;
                        this.form.zone_id = res.dns_record.zone_id;
                        this.form.sort = res.dns_record.sort;
                    })
                    .catch((e) => {
                        console.log(e);
                        throw e;
                    });
            } else {
                dnsRecord
                    .getDnsRecord(this.dnsRecordId)
                    .then((res) => {
                        this.isLoaded = true;
                        this.form.record = res.dns_record.record;
                        this.form.sort = res.dns_record.sort;
                        this.form.zone_id = res.dns_record.zone_id;
                    })
                    .catch((e) => {
                        console.log(e);
                        throw e;
                    });
            }
        } else {
            this.isLoaded = true;
        }
    }

    mounted() {
        this.boot();
    }
}
</script>
