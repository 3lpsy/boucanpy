import { Route } from 'vue-router';
import Guard from '@/router/guards/guard';
import Token from '@/services/token';

export class HasAuthenticationCookie extends Guard {
    protect(to: Route, from: Route, next: any): void {
        console.log('Running Guard', this);
        if (!Token.exists()) {
            console.log('No token found. Redirecting');
            next({ name: 'login' });
        }
        next();
    }
}

export class IsAuthenticated extends Guard {
    protect(to: Route, from: Route, next: any): void {
        console.log('Running Guard', this);
        next();
    }
}
