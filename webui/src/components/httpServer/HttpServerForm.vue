<template id="">
    <b-form @submit.prevent="onSubmit" v-if="isLoaded">
        <b-form-group
            label="Name"
            label-for="input-name"
            description="The HTTP Server name"
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
        <p v-if="mode=='edit'">
            <em>*Note: Changing the name for a server after a token has been generated may deauth the server.</em>
        </p>
        <button class="btn btn-lg btn-primary pull-right">Submit</button>
    </b-form>
</template>

<script>
import Component from 'vue-class-component';
import { mixins } from 'vue-class-component';
import uuid4 from 'uuid4';

import CommonMixin from '@/mixins/common';

import httpServer from '@/services/httpServer';
import moment from 'moment';
import bus from '@/bus';

@Component({
    props: {
        mode: {
            type: String,
            default: 'create',
        },
        httpServerId: {
            type: Number,
            default: 0,
        },
    },
})
export default class HttpServerCreateForm extends mixins(CommonMixin) {
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
                            httpServer
                                .updateHttpServer(this.httpServerId, data)
                                .then(() => {
                                    console.log('emiting app event');
                                    bus.$emit('APP_ALERT', {
                                        text: 'Http Server Created',
                                        type: 'success',
                                    });
                                    bus.$emit('HTTP_SERVER_UPDATED');
                                    this.disabled = false;
                                    this.$router.push({ name: 'server' });
                                })
                                .catch((e) => {
                                    this.disabled = false;
                                    throw e;
                                });
                        } else {
                            httpServer
                                .createHttpServer(data)
                                .then(() => {
                                    console.log('emiting app event');
                                    bus.$emit('APP_ALERT', {
                                        text: 'Http Server Created',
                                        type: 'success',
                                    });
                                    bus.$emit('HTTP_SERVER_CREATED');
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
            // check to make sure httpServer exists for edit form and load data
            httpServer
                .getHttpServer(this.httpServerId)
                .then((res) => {
                    this.isLoaded = true;
                    this.form.name = res.http_server.name;
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
