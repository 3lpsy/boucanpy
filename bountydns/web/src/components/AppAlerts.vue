
<template>
  <div class="alerts-section row">
      <div class="container-fluid">

      <b-alert
        dismissible
        :show="true"
        :max="30"
        :variant="alert.type || 'info'"
        v-on:dismissed="removeAlert(alert)"
        :key="index"
        v-for="(alert, index) in alerts" v-if="alerts.length > 0"
    >
          {{ alert.text }}
      </b-alert>
  </div>
  </div>
</template>

<script>
import { Vue, Component } from 'vue-property-decorator';
import bus from '@/bus';

@Component
export default class AppAlerts extends Vue {
    alerts = []

    removeAlert(alert) {
        console.log("Remving alert", alert)
        this.alerts = this.alerts.filter((a) => a != alert )
    }
    mounted() {
        bus.$on("APP_ALERT", (payload) => {
            console.log("Received alert", payload)
            this.alerts.push(payload)
        })
    }
}
</script>

<style media="screen">

</style>
