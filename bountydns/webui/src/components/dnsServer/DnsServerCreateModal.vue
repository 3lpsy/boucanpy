<template id="">
    <b-modal ref="form-modal" size="lg" hide-footer id="create-dns-server" title="Create Dns Server">
        <dns-server-create-form v-on:form-complete="closeModal"></dns-server-create-form>
    </b-modal>
</template>

<script>
import Component from 'vue-class-component'
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
import DnsServerMixin from '@/mixins/dnsServer';
import DnsServerCreateForm from '@/components/dnsServer/DnsServerCreateForm.vue';

@Component({
    props: {
        modalId: {
            type: String
        }
    },
    components: {DnsServerCreateForm}
})
export default class DnsServerCreateModal extends mixins(CommonMixin, DnsServerMixin) {

    closeModal() {
        this.$refs['form-modal'].hide()
     }

}
</script>
