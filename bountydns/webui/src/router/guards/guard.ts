import { Route } from 'vue-router';

export class IGuard {
    protect(to: Route, from: Route, next: any): void {}
}

export default class Guard implements IGuard {
    constructor() {}
    protect(to: Route, from: Route, next: any): void {}
}
