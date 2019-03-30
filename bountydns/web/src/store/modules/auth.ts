import {
    Module,
    VuexModule,
} from 'vuex-module-decorators';
import store from '@/store';
import { User, Token } from '@/types';

@Module({
    namespaced: true,
    name: 'auth',
    store,
})
class AuthModule extends VuexModule {
    user: User | null = null;
    token: Token | null = null;
}

export default AuthModule;
