import { ActionContext } from 'vuex';
import { IAuthState } from './state';
import { IState } from '@/store/state';

import { User, LoginForm, UserResponse } from '@/types';
import authService from '@/services/auth';
import tokenService from '@/services/token';
import * as api from '@/services/api';
import broadcast from '@/broadcast';

export interface IAuthActions {
    loadUser(context: ActionContext<IAuthState, IState>): Promise<User>;
    authenticate(
        context: ActionContext<IAuthState, IState>,
        form: LoginForm,
    ): Promise<User>;

    setUpAccessToken(
        context: ActionContext<IAuthState, IState>,
        token: string,
    ): Promise<User>;

    setUpWSAccessToken(
        context: ActionContext<IAuthState, IState>,
        token: string,
    ): Promise<string>;

    deauthenticate(context: ActionContext<IAuthState, IState>): Promise<void>;
    refresh(
        context: ActionContext<IAuthState, IState>,
        token: string,
    ): Promise<string>;
    refreshWS(
        context: ActionContext<IAuthState, IState>,
        token: string,
    ): Promise<string>;
}

export const AuthActions: IAuthActions = {
    loadUser({ commit }): Promise<User> {
        return new Promise((resolve, reject) => {
            authService
                .getUser()
                .then((userResponse: UserResponse) => {
                    let user = userResponse.user;
                    commit('SET_USER', user);
                    resolve(user);
                })
                .catch((err) => {
                    console.log('loadUser error');
                    reject(err);
                });
        });
    },

    refresh({ dispatch }, token: string): Promise<string> {
        console.log('auth/refresh');
        return new Promise((resolve, reject) => {
            authService
                .refresh(token)
                .then((token: any) => {
                    console.log('dispatching auth/setUpAccessToken');
                    dispatch('setUpAccessToken', token)
                        .then((user: User) => {
                            resolve(token);
                        })
                        .catch((err: any) => {
                            console.log('Refresh Error:', err);
                            reject(err);
                        });
                })
                .catch((err) => {
                    console.log('refresh error');
                    console.log('dispatching auth/deauthenticate');
                    return new Promise((resolve, reject) => {
                        dispatch('deauthenticate').then(() => {
                            reject(err);
                        });
                    });
                });
        });
    },

    refreshWS({ dispatch }, token: string): Promise<string> {
        console.log('auth/refreshWS');
        return new Promise((resolve, reject) => {
            authService
                .refresh(token)
                .then((token: any) => {
                    console.log('dispatching auth/setUpWSAccessToken');
                    dispatch('setUpWSAccessToken', token)
                        .then((user: User) => {
                            resolve(token);
                        })
                        .catch((err: any) => {
                            console.log('Refresh WS Error:', err);
                            reject(err);
                        });
                })
                .catch((err) => {
                    console.log('refresh error');
                    console.log('dispatching auth/deauthenticate');
                    return new Promise((resolve, reject) => {
                        dispatch('deauthenticate').then(() => {
                            reject(err);
                        });
                    });
                });
        });
    },

    authenticate({ dispatch }, form: LoginForm): Promise<User> {
        console.log('auth/authenticate', form);

        return new Promise((resolve, reject) => {
            authService
                .login(form)
                .then((tokens: any) => {
                    console.log('dispatching auth/setUpAccessToken');
                    dispatch('setUpAccessToken', tokens.accessToken)
                        .then((user) => {
                            if (tokens.wsAccessToken) {
                                dispatch(
                                    'setUpWSAccessToken',
                                    tokens.wsAccessToken,
                                )
                                    .then((token) => {
                                        resolve(user);
                                    })
                                    .catch((err) => {
                                        console.log(
                                            'auth/setUpWSAccessToken error in auth/authenticate:',
                                            err,
                                        );
                                        throw err;
                                    });
                            } else {
                                resolve(user);
                            }
                        })
                        .catch((err) => {
                            console.log(
                                'auth/setUpAccessToken error in auth/authenticate:',
                                err,
                            );
                            throw err;
                        });
                })
                .catch((err) => {
                    console.log('authenticate error');
                    console.log('dispatching auth/deauthenticate');
                    dispatch('deauthenticate').then(() => {
                        reject(err);
                    });
                });
        });
    },

    setUpAccessToken({ dispatch, commit }, token: string): Promise<User> {
        console.log('auth/setUpAccessToken', token);

        return new Promise((resolve, reject) => {
            tokenService.save(token);

            let parsedAccessToken = tokenService.parse(token);
            commit('SET_TOKEN', parsedAccessToken);
            api.setServiceToken(parsedAccessToken.token);
            return dispatch('loadUser')
                .then((user) => {
                    resolve(user);
                })
                .catch((err) => {
                    console.log(
                        'auth/loadUser Error in setUpAccessToken:',
                        err,
                    );
                    throw err;
                });
        });
    },

    setUpWSAccessToken({ dispatch, commit }, token: string): Promise<string> {
        console.log('auth/setUpWSAccessToken');
        return new Promise((resolve, reject) => {
            tokenService.saveWS(token);
            let parsedWSAccessToken = tokenService.parse(token);
            commit('SET_WS_TOKEN', parsedWSAccessToken);
            if (parsedWSAccessToken.token) {
                console.log('enabling authws');
                broadcast.registerAuthedWS(token);
            }
            resolve(token);
        });
    },

    deauthenticate({ commit }): Promise<void> {
        console.log('auth/deauthenticate');

        return new Promise((resolve, reject) => {
            commit('CLEAR_TOKEN');
            commit('CLEAR_WS_TOKEN');

            commit('CLEAR_USER');
            tokenService.remove();
            api.clearServiceToken();
            resolve();
        });
    },
};
