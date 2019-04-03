import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';

import VueBootstrapTypeahead from 'vue-bootstrap-typeahead';

Vue.use(BootstrapVue);
Vue.component('vue-bootstrap-typeahead', VueBootstrapTypeahead);

import App from './App.vue';
import router from '@/router';
import { store } from './store';

// import { WS_URL } from '@/config';

Vue.config.productionTip = false;

const vm = new Vue({
    router,
    store,
    render: (h) => h(App),
}).$mount('#app');
