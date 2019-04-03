import { IAuthState } from './state';
import { Token, User } from '@/types';

export interface IAuthGetters {
    isAuthenticated(state: IAuthState): boolean;
    getToken(state: IAuthState): Token;
    getUser(state: IAuthState): User;
    hasToken(state: IAuthState): boolean;
    hasUser(state: IAuthState): boolean;
    hasWSTokenRaw(state: IAuthState): boolean;
    getWSTokenRaw(state: IAuthState): string;

}

export const AuthGetters: IAuthGetters = {
    isAuthenticated(state: IAuthState): boolean {
        if (! state.user || state.user.id < 1) {
            return false
        }
        else if (state.token.sub.length < 1) {
            return false
        }
        return true
    },

    hasToken(state: IAuthState): boolean {
        if (! state.token || state.token.sub.length < 1) {
            return false
        }
        return true
    },

    hasUser(state: IAuthState): boolean {
        if (! state.user || state.user.id < 1) {
            return false
        }
        return true
    },

    getToken(state: IAuthState): Token {
        return state.token
    },

    getUser(state: IAuthState): User {
        return state.user
    },

    getWSTokenRaw(state: IAuthState): string {
        return state.wsTokenRaw
    },
    hasWSTokenRaw(state: IAuthState): boolean {
        return state.wsTokenRaw.length > 0
    },
};
