// mixin.js
import Vue from 'vue';
import Component from 'vue-class-component';
import moment from 'moment';

// You can declare a mixin as the same style as components.
@Component
export default class DataTableMixin extends Vue {
    isLoaded = false;
    currentPage = 0;
    perPage = 20;
    total = 0;
    sortBy = 'id';
    sortDesc = false;
    items = [];

    changeSort(sort: any) {
        this.sortBy = sort.sortBy;
        this.sortDesc = sort.sortDesc;
        this.loadData();
    }

    changePage(page: any) {
        this.currentPage = page;
        this.loadData();
    }

    loadData() {}

    formatDate(dt: number) {
        return moment(dt).format('YYYY-MM-DD HH:mm:ss');
    }

    mounted() {
        this.loadData();
    }
}
