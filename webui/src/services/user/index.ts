import qs from 'qs';
import * as api from '@/services/api';
import { UsersResponse, UserResponse, UserCreateForm } from '@/types';
import { IGeneralQS } from '@/queries';

class UserService {
    getUsers(query: IGeneralQS): Promise<UsersResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .get('/user', { params: query })
                .then((response: any) => {
                    let responseData = response.data as UsersResponse;
                    resolve(responseData);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }

    getUser(userId: number, includes?: string[]): Promise<UserResponse> {
        return new Promise((resolve, reject) => {
            let query = { includes: includes };
            api.http
                .get(`/user/${userId}`, { params: query })
                .then((response: any) => {
                    let responseData = response.data as UserResponse;
                    resolve(responseData);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }

    createUser(form: UserCreateForm): Promise<UserResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .post('/user', form)
                .then((response: any) => {
                    let responseData = response.data as UserResponse;
                    resolve(responseData);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }

    updateUser(userId: number, form: UserCreateForm): Promise<UserResponse> {
        return new Promise((resolve, reject) => {
            api.http
                .put(`/user/${userId}`, form)
                .then((response: any) => {
                    let responseData = response.data as UserResponse;
                    resolve(responseData);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }

    deactivateUser(userId: number): Promise<any> {
        return new Promise((resolve, reject) => {
            api.http
                .delete(`/user/${userId}`)
                .then((response: any) => {
                    let responseData = response.data as UserResponse;
                    resolve(responseData);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }

    activateUser(userId: number): Promise<any> {
        return new Promise((resolve, reject) => {
            api.http
                .put(`/user/${userId}/activate`)
                .then((response: any) => {
                    let responseData = response.data as UserResponse;
                    resolve(responseData);
                })
                .catch((err) => {
                    reject(err);
                });
        });
    }
}

export default new UserService();
