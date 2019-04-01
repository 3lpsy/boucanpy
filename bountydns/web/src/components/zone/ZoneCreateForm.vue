<template id="">
    <b-form @submit="onSubmit">
        <fieldset class="form-group">
            <label for="input-domain">Zone Domain</label>
            <input
                id="input-domain"
                type="text"
                placeholder="example.com"
                class="form-control form-control-lg"
                v-model="form.domain"
            >
            <small>The DNS Server will create multiple rules based off the domain. Non Zone requests will still be logged.</small>
        </fieldset>
        <fieldset class="form-group">
            <label for="input-ip">Resolve IP</label>
            <input
                id="input-ip"
                type="text"
                placeholder="127.0.0.1"
                class="form-control form-control-lg"
                v-model="form.ip"
            >
            <small>The IP to Answer with for Relevant DNS Requests.</small>
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
import CommonMixin from '@/mixins/common';
import ZoneMixin from '@/mixins/zone';
import zone from '@/services/zone';
import bus from '@/bus';

@Component()
export default class ZoneCreateForm extends mixins(CommonMixin, ZoneMixin) {
    formError = ''
    form = {
        'domain': '',
        'ip': ''
    }
    onSubmit() {
        console.log('submitting data', this.form)
        zone.createZone(this.form).then(() => {
            console.log("emiting app event")
            bus.$emit('APP_ALERT', {text: "Zone Created", type: "success"})
            console.log("emiting formComplete event")
            this.$emit('form-complete')
        })
    }



    mounted() {
    }
}
</script>
