import Vue from 'vue';

import VeeValidate from 'vee-validate';

const config = {
    aria: true,
    classNames: {},
    classes: false,
    delay: 0,
    dictionary: null,
    errorBagName: 'veeErrorBag', // change if property conflicts
    events: 'input|blur',
    fieldsBagName: 'veeInputBag',
    i18n: null, // the vue-i18n plugin instance
    i18nRootKey: 'validations', // the nested key under which the validation messages will be located
    inject: true,
    locale: 'en',
    validity: false,
    useConstraintAttrs: true,
};

Vue.use(VeeValidate, config);

import BootstrapVue from 'bootstrap-vue';

import VueBootstrapTypeahead from 'vue-bootstrap-typeahead';

Vue.use(BootstrapVue);
Vue.component('vue-bootstrap-typeahead', VueBootstrapTypeahead);

import App from './App.vue';
import router from '@/router';
import { store } from './store';
import broadcast from '@/broadcast';

broadcast.registerPublicWS();

Vue.config.productionTip = false;

new Vue({
    router,
    store,
    render: (h) => h(App),
}).$mount('#app');
