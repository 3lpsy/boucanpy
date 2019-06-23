import { User, Token } from '@/types';

export interface IAuthState {
    user: User;
    token: Token;
    wsToken: Token;
}

export const AuthDefaultState = (): IAuthState => {
    return {
        user: {
            id: 0,
            email: '',
            created_at: 0,
            is_superuser: false,
            is_active: false,
        },
        token: { sub: '', exp: 0, scopes: [], token: '' },
        wsToken: { sub: '', exp: 0, scopes: [], token: '' },
    };
};
