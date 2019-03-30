import { Route } from 'vue-router';
import Guard from '@/router/guards/guard';

// TODO: Fix this nonsense
const perform = (
    guards: Guard[],
    to: Route,
    from: Route,
    finalNext: any,
    i: number,
) => {
    let guard = guards[i];
    console.log('Performing with guard', guard);
    if (guards.length === i + 1) {
        console.log('Guard is last of the guards, passing finalNext');
        guard.protect(from, to, finalNext);
    } else {
        guard.protect(from, to, function(nextArg: any) {
            if (typeof nextArg === 'undefined') {
                // next was called without arguments
                console.log('Recalling perform with an increaseed index');
                perform(guards, from, to, finalNext, i + 1);
            } else if (
                ['object', 'boolean', 'string'].includes(typeof nextArg)
            ) {
                // next was called with arguments (jump out)
                console.log('Calling finalNext', nextArg);
                finalNext(nextArg);
                return;
            }
        });
    }
};

const GuardCollection = (guards: Guard[]) => {
    if (!guards || guards.length < 1) {
        return function(to: Route, from: Route, next: any) {
            next();
        };
    }
    return function(to: Route, from: Route, next: any) {
        perform(guards, from, to, next, 0);
    };
};

export default GuardCollection;
