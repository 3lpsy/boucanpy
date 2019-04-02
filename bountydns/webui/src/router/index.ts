import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/views/Home.vue';
import Zone from '@/views/Zone.vue';
import ApiToken from '@/views/ApiToken.vue';
import Login from '@/views/Login.vue';
import Chat from '@/views/Chat.vue';

import NotFound from '@/views/errors/NotFound.vue';

import GuardCollection from '@/router/guards/collection';
import { HasAuthenticationCookie, IsAuthenticated } from '@/router/guards/auth';

const AUTHED_GUARDS = GuardCollection([
    new HasAuthenticationCookie(),
    new IsAuthenticated(),
]);

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/zone',
            name: 'zone',
            component: Zone,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/api-token',
            name: 'api-token',
            component: ApiToken,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/chat',
            name: 'chat',
            component: Chat,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/login',
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
