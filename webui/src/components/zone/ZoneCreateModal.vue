<template id="">
    <b-modal
        ref="form-modal"
        size="lg"
        hide-footer
        id="create-zone"
        title="Create Resolvable Zone"
    >
        <zone-form mode="create" v-on:form-complete="closeModal"></zone-form>
    </b-modal>
</template>

<script>
import Component from 'vue-class-component';
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
import ZoneMixin from '@/mixins/zone';
import ZoneForm from '@/components/zone/ZoneForm.vue';

@Component({
    props: {
        modalId: {
            type: String,
        },
    },
    components: { ZoneForm },
})
export default class ZoneCreateModal extends mixins(CommonMixin, ZoneMixin) {
    closeModal() {
        this.$refs['form-modal'].hide();
    }
}
</script>
