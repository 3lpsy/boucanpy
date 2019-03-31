
import { User, Token} from '@/types';

export interface IAuthState {
  user: User;
  token: Token;
}

export const AuthDefaultState = (): IAuthState => {
    return {
        user: {id: 0, email: ''},
        token: {sub: '', exp: '', scopes: []}
    };
};
