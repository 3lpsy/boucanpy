import { IAuthState } from './state';
import { Token, User } from '@/types';

export interface IAuthMutations {
    CLEAR_TOKEN(state: IAuthState): void;
    CLEAR_WS_TOKEN(state: IAuthState): void;

    SET_TOKEN(state: IAuthState, token: Token): void;
    CLEAR_USER(state: IAuthState): void;
    SET_USER(state: IAuthState, user: User): void;
    SET_WS_TOKEN(state: IAuthState, wsToken: Token): void;
}

export const AuthMutations: IAuthMutations = {
    CLEAR_TOKEN: (state) => {
        state.token = { sub: '', exp: 0, scopes: [], token: '' };
    },
    CLEAR_WS_TOKEN: (state) => {
        state.wsToken = { sub: '', exp: 0, scopes: [], token: '' };
    },
    SET_TOKEN: (state, token: Token) => {
        state.token = token;
    },
    SET_WS_TOKEN: (state, wsToken: Token) => {
        state.wsToken = wsToken;
    },
    CLEAR_USER: (state) => {
        state.user = {
            id: 0,
            email: '',
            created_at: 0,
            is_superuser: false,
            is_active: false,
        };
    },
    SET_USER: (state, user: User) => {
        state.user = user;
    },
};
