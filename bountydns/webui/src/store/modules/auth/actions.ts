import { ActionContext } from 'vuex';
import { IAuthState } from './state';
import { IState } from '@/store/state';

import { User, LoginForm, UserResponse} from '@/types';
import authService from '@/services/auth';
import tokenService from '@/services/token';
import * as api from '@/services/api';


export interface IAuthActions {
    loadUser(context: ActionContext<IAuthState, IState>):  Promise<User>;
    authenticate(context: ActionContext<IAuthState, IState>, form: LoginForm):  Promise<User>;
    authenticateWithToken(context: ActionContext<IAuthState, IState>, accessToken: string):  Promise<User>;
    deauthenticate(context: ActionContext<IAuthState, IState>): Promise<void>;
    refresh(context: ActionContext<IAuthState, IState>): Promise<string>;

}

export const AuthActions: IAuthActions = {

    loadUser({ commit }): Promise<User>  {
        return new Promise((resolve, reject) => {
            authService.getUser().then((userResponse: UserResponse) => {
                let user = userResponse.user
                commit('SET_USER', user)
                resolve(user)
            }).catch((err) => {
                console.log("loadUser error")
                reject(err);
            })
        });

    },

    refresh({ dispatch, commit }): Promise<string> {
        console.log('auth/refresh')
        return new Promise((resolve, reject) => {
            authService
              .refresh()
              .then((accessToken: string) => {
                  console.log('dispatching auth/authenticateWithToken')
                  dispatch('authenticateWithToken', accessToken).then((user) => {
                      resolve(accessToken)
                  }).catch((err) => {
                      reject(err)
                  })
              }).catch((err) => {
                  console.log("refresh error")
                  console.log("dispatching auth/deauthenticate")
                  return new Promise((resolve, reject) => {
                      dispatch('deauthenticate').then(() => {
                          reject(err)
                      })
                  })
              });
        })

    },

    authenticate({ dispatch, commit }, form: LoginForm): Promise<User> {
        console.log('auth/authenticate')
        return authService
          .login(form)
          .then((accessToken: string) => {
              console.log('dispatching auth/authenticateWithToken')
              return dispatch('authenticateWithToken', accessToken)
          }).catch((err) => {
              console.log("authenticate error")
              console.log("dispatching auth/deauthenticate")
              return new Promise((resolve, reject) => {
                  dispatch('deauthenticate').then(() => {
                      reject(err)
                  })
              })
          });
    },

    authenticateWithToken({ dispatch, commit }, accessToken: string): Promise<User> {
        console.log('auth/authenticateWithToken')
        let token = tokenService.parse(accessToken)
        tokenService.save(accessToken)
        commit('SET_TOKEN', token)
        api.setServiceToken(accessToken)
        return dispatch('loadUser')
    },

    deauthenticate({ commit }): Promise<void>  {
        return new Promise((resolve, reject) => {
            commit('CLEAR_TOKEN')
            commit('CLEAR_USER')
            tokenService.remove()
            api.clearServiceToken()
            resolve()
        })
    }
}
