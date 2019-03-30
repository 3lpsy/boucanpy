import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/views/Home.vue';
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
            path: '/login',
            name: 'login',
            component: () => import('@/views/Login.vue'),
        },
    ],
});
