// mixin.js
import Vue from 'vue';
import Component from 'vue-class-component';

// You can declare a mixin as the same style as components.
@Component
export default class ApiTokenMixin extends Vue {
    isLoaded = false
    currentPage = 0
    perPage = 20
    items = []

    get itemCount() {
        return this.items.length
    }
}
