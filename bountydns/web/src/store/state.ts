import { AuthDefaultState, IAuthState } from '@/store/modules/auth/state';

export interface IState {
  [key: string]: any;
  auth?: IAuthState;
}

export const DefaultState: IState = {
};
