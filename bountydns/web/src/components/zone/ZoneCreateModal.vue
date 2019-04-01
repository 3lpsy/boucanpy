<template id="">
    <b-modal ref="form-modal" size="lg" hide-footer id="create-zone" title="Create Resolvable Zone">
        <zone-create-form v-on:form-complete="closeModal"></zone-create-form>
    </b-modal>
</template>

<script>
import Component from 'vue-class-component'
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
import ZoneMixin from '@/mixins/zone';
import ZoneCreateForm from '@/components/zone/ZoneCreateForm.vue';

@Component({
    props: {
        modalId: {
            type: String
        }
    },
    components: {ZoneCreateForm}
})
export default class ZoneCreateModal extends mixins(CommonMixin, ZoneMixin) {

    closeModal() {
        console.log("Closing modal")
        this.$refs['form-modal'].hide()
     }

}
</script>
