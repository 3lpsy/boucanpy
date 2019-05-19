import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/views/Home.vue';
import Server from '@/views/Server.vue';

import Zone from '@/views/Zone.vue';
import ZoneEdit from '@/views/ZoneEdit.vue';

import ApiToken from '@/views/ApiToken.vue';
import Login from '@/views/Login.vue';

import NotFound from '@/views/errors/NotFound.vue';

import GuardCollection from '@/router/guards/collection';
import { HasAuthenticationCookie, IsAuthenticated } from '@/router/guards/auth';

const AUTHED_GUARDS = GuardCollection([
    new HasAuthenticationCookie(),
    new IsAuthenticated(),
]);

Vue.use(Router);

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/webui',
            name: 'home',
            component: Home,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/server',
            name: 'server',
            component: Server,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/zone',
            name: 'zone',
            component: Zone,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/zone/:zoneId',
            name: 'zone.edit',
            component: ZoneEdit,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/api-token',
            name: 'api-token',
            component: ApiToken,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/login',
            name: 'login',
            component: Login,
        },
        {
            path: '*',
            name: '404',
            component: NotFound,
        },
    ],
});
