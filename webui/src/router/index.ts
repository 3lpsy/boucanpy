import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/views/Home.vue';

import Server from '@/views/Server.vue';
import DnsServerCreate from '@/views/DnsServerCreate.vue';
import DnsServerEdit from '@/views/DnsServerEdit.vue';
import DnsServerShow from '@/views/DnsServerShow.vue';

import UserIndex from '@/views/UserIndex.vue';
import UserCreate from '@/views/UserCreate.vue';
import UserEdit from '@/views/UserEdit.vue';

import ProfileEdit from '@/views/ProfileEdit.vue';

import Zone from '@/views/Zone.vue';
import ZoneEdit from '@/views/ZoneEdit.vue';
import ZoneCreate from '@/views/ZoneCreate.vue';

import ZoneShow from '@/views/ZoneShow.vue';
import ZoneDnsRecordCreate from '@/views/ZoneDnsRecordCreate.vue';
import ZoneDnsRecordEdit from '@/views/ZoneDnsRecordEdit.vue';

import ApiToken from '@/views/ApiToken.vue';
import ApiTokenCreate from '@/views/ApiTokenCreate.vue';
import ApiTokenEdit from '@/views/ApiTokenEdit.vue';

import DnsRequestShow from '@/views/DnsRequestShow.vue';

import HttpServerCreate from '@/views/HttpServerCreate.vue';
import HttpServerEdit from '@/views/HttpServerEdit.vue';
import HttpServerShow from '@/views/HttpServerShow.vue';
import HttpRequestShow from '@/views/HttpRequestShow.vue';

import Login from '@/views/Login.vue';

import NotFound from '@/views/errors/NotFound.vue';

import GuardCollection from '@/router/guards/collection';
import {
    HasAuthenticationCookie,
    IsAuthenticated,
    IsSuperuser,
} from '@/router/guards/auth';

const AUTHED_GUARDS = GuardCollection([
    new HasAuthenticationCookie(),
    new IsAuthenticated(),
]);

const SUPER_GUARDS = GuardCollection([
    new HasAuthenticationCookie(),
    new IsAuthenticated(),
    new IsSuperuser(),
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
            path: '/webui/user',
            name: 'user.index',
            component: UserIndex,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/user/create',
            name: 'user.create',
            component: UserCreate,
            beforeEnter: SUPER_GUARDS,
        },
        {
            path: '/webui/user/:userId/edit',
            name: 'user.edit',
            component: UserEdit,
            beforeEnter: AUTHED_GUARDS,
        },

        {
            path: '/webui/profile/edit',
            name: 'profile.edit',
            component: ProfileEdit,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/server',
            name: 'server',
            component: Server,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/dns-server/create',
            name: 'dns-server.create',
            component: DnsServerCreate,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/dns-server/:dnsServerId',
            name: 'dns-server.show',
            component: DnsServerShow,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/dns-server/:dnsServerId/edit',
            name: 'dns-server.edit',
            component: DnsServerEdit,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/dns-request/:dnsRequestId',
            name: 'dns-request.show',
            component: DnsRequestShow,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/zone/:zoneId/dns-record/create',
            name: 'zone.dns-record.create',
            component: ZoneDnsRecordCreate,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/zone/:zoneId/dns-record/:dnsRecordId/edit',
            name: 'zone.dns-record.edit',
            component: ZoneDnsRecordEdit,
            beforeEnter: AUTHED_GUARDS,
        },

        {
            path: '/webui/zone',
            name: 'zone',
            component: Zone,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/zone/create',
            name: 'zone.create',
            component: ZoneCreate,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/zone/:zoneId',
            name: 'zone.show',
            component: ZoneShow,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/zone/:zoneId/edit',
            name: 'zone.edit',
            component: ZoneEdit,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/api-token/:apiTokenId/edit',
            name: 'api-token.edit',
            component: ApiTokenEdit,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/api-token/create',
            name: 'api-token.create',
            component: ApiTokenCreate,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/api-token',
            name: 'api-token',
            component: ApiToken,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/http-server/create',
            name: 'http-server.create',
            component: HttpServerCreate,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/http-server/:httpServerId',
            name: 'http-server.show',
            component: HttpServerShow,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/http-server/:httpServerId/edit',
            name: 'http-server.edit',
            component: HttpServerEdit,
            beforeEnter: AUTHED_GUARDS,
        },
        {
            path: '/webui/http-request/:httpRequestId',
            name: 'http-request.show',
            component: HttpRequestShow,
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
