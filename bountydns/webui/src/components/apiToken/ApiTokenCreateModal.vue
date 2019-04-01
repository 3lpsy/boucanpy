<template id="">
    <b-modal ref="form-modal" size="lg" hide-footer id="create-api-token" title="Create API Token">
        <api-token-create-form v-on:form-complete="closeModal"></api-token-create-form>
    </b-modal>
</template>

<script>
import Component from 'vue-class-component'
import { mixins } from 'vue-class-component';
import CommonMixin from '@/mixins/common';
import ApiTokenMixin from '@/mixins/apiToken';
import apiToken from '@/services/apiToken';
import ApiTokenCreateForm from '@/components/apiToken/ApiTokenCreateForm.vue';

@Component({
    props: {
        modalId: {
            type: String
        }
    },
    components: {ApiTokenCreateForm}
})
export default class ApiTokensCreateModal extends mixins(CommonMixin, ApiTokenMixin) {

    closeModal() {
        console.log("Closing modal")
        this.$refs['form-modal'].hide()
     }

}
</script>
