import { IAuthState } from './state';
import { Token, User } from '@/types';

export interface IAuthGetters {
    isAuthenticated(state: IAuthState): boolean;
    getToken(state: IAuthState): Token;
    getUser(state: IAuthState): User;
    hasToken(state: IAuthState): boolean;
    hasUser(state: IAuthState): boolean;

}

export const AuthGetters: IAuthGetters = {
    isAuthenticated(state: IAuthState): boolean {
        if (state.user.id < 1) {
            return false
        }
        else if (state.token.sub.length < 1) {
            return false
        }
        return true
    },

    hasToken(state: IAuthState): boolean {
        if (state.token.sub.length < 1) {
            return false
        }
        return true
    },

    hasUser(state: IAuthState): boolean {
        if (state.user.id < 1) {
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
};
