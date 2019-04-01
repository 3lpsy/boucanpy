<template id="">
    <b-form @submit="onSubmit">
        <fieldset class="form-group">
            <label for="input-scopes">Scopes</label>
            <input
                id="input-scopes"
                type="text"
                placeholder="Scopes"
                class="form-control form-control-lg"
                v-model="form.scopes"
            >
            <small>Note: The 'dns-request' or 'dns-request:create' (same for dns-response) scopes are required for the DNS server</small>
        </fieldset>
        <fieldset class="form-group">
            <label for="input-exp">Expiration</label>
            <input
                id="input-exp"
                type="date"
                placeholder="Scopes"
                class="form-control form-control-lg"
                v-model="form.expires_at"
            >
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
import ApiTokenMixin from '@/mixins/apiToken';
import apiToken from '@/services/apiToken';
import moment from 'moment';
import bus from '@/bus';

@Component()
export default class ApiTokensCreateForm extends mixins(CommonMixin, ApiTokenMixin) {
    formError = ''
    form = {
        'scopes': '',
        'expires_at': ''
    }
    onSubmit() {
        let data = {scopes: this.form.scopes, expires_at: moment(this.form.expires_at, 'YYYY-MM-DD').unix()}
        console.log('submitting data', data)
        apiToken.createApiToken(data).then(() => {
            console.log("emiting app event")
            bus.$emit('APP_ALERT', {text: "Api Token Created", type: "success"})
            console.log("emiting formComplete event")
            this.$emit('form-complete')
        })
    }



    mounted() {
        this.form.scopes = this.$store.getters['auth/getToken'].scopes.join(' ')
        this.form.expires_at = moment().add(90, 'days').format('YYYY-MM-DD');
    }
}
</script>
