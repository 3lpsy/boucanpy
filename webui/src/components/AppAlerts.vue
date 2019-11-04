
<template>
    <div class="alerts-section row">
        <div class="container-fluid">
            <b-alert
                dismissible
                fade
                :show="alert.show > 0"
                :max="30"
                :variant="alert.type || 'info'"
                v-on:dismissed="removeAlert(alert)"
                :key="index"
                v-for="(alert, index) in alerts"
                v-if="alerts.length > 0"
                style="margin-bottom: 0px"
            >{{ alert.text }}</b-alert>
        </div>
    </div>
</template>

<script>
import Vue from 'vue';
import Component from 'vue-class-component';
import bus from '@/bus';

@Component({})
export default class AppAlerts extends Vue {
    alerts = [];
    registeredEvents = [];

    removeAlert(alert) {
        console.log('Remving alert', alert);
        this.alerts = this.alerts.filter((a) => a != alert);
        alert.show = false;
    }

    registerOnAlert() {
        console.log('registering APP_ALERT event on bus');
        if (!this.registeredEvents.includes('APP_ALERT')) {
            console.log('registering APP_ALERT event on bus');
            bus.$on('APP_ALERT', (alert) => {
                console.log('receving app alert', alert);
                if (alert.show === null || alert.show === undefined) {
                    alert.show = true;
                }
                if (alert.timeout === null || alert.timeout === undefined) {
                    alert.timeout = 10;
                }
                this.alerts.push(alert);
                setTimeout(
                    function() {
                        this.removeAlert(alert);
                    }.bind(this),
                    alert.timeout * 1000,
                );
            });
            this.registeredEvents.push('APP_ALERT');
        }
    }

    registerOnToast() {
        if (!this.registeredEvents.includes('APP_TOAST')) {
            bus.$on('APP_TOAST', (toast) => {
                this.$bvToast.toast(toast.message, toast.options);
            });
            this.registeredEvents.push('APP_TOAST');
        }
    }

    created() {
        this.registerOnAlert();
        this.registerOnToast();
    }
}
</script>

<style media="screen">
</style>
