import { IAuthState } from './state';
import { Token, User } from '@/types';

export interface IAuthMutations {
    CLEAR_TOKEN(state: IAuthState): void;
    SET_TOKEN(state: IAuthState, token: Token): void;
    CLEAR_USER(state: IAuthState): void;
    SET_USER(state: IAuthState, user: User): void;
}

export const AuthMutations: IAuthMutations = {
    CLEAR_TOKEN: (state) => {
        state.token = { sub: '', exp: '', scopes: [] };
    },
    SET_TOKEN: (state, token: Token) => {
        state.token = token;
    },
    CLEAR_USER: (state) => {
        state.user = { id: 0, email: '', created_at: 0 };
    },
    SET_USER: (state, user: User) => {
        state.user = user;
    },
};
