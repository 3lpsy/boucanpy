import Vue from 'vue';
import Vuex, { Module, Store } from 'vuex';
import merge from 'deepmerge';
import { DefaultState, IState } from './state';
import { AuthModule } from '@/store/modules/auth/module';

const state: IState = DefaultState;

Vue.use(Vuex);

export const store: Store<IState> = new Vuex.Store({
    state: state,
});

export const registerModule = (moduleName: string, module: Module<any, any>) => {
  const moduleIsRegistered: boolean = (store as any)._modules.root._children[moduleName] !== undefined;
  const stateExists: boolean = store.state[moduleName] !== undefined;

  if (stateExists) {
    module.state = merge(module.state, store.state[moduleName], {
      clone: false,
      arrayMerge: /* istanbul ignore next */ (target: any, source: any) => {
        return source;
      },
    });
  }

  if (!moduleIsRegistered) {
      store.registerModule(moduleName, module, { preserveState: false });
  }
};

registerModule('auth', AuthModule);
