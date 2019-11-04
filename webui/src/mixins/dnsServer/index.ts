// mixin.js
import Vue from 'vue';
import Component from 'vue-class-component';
import { DnsServersResponse } from '@/types';
import dnsServer from '@/services/dnsServer';
// You can declare a mixin as the same style as components.
@Component({})
export default class DnsServersMixin extends Vue {}
