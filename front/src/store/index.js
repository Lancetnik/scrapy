import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import Cookies from 'js-cookie'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    backendUrl: "http://127.0.0.1:8000",
    token: null,
    jwtToken: null,
    refreshToken: null,

    filter: null
  },

  mutations: {
    setToken (state, value) {
      state.token = value
    },

    setJwt (state, tokens) {
      state.jwtToken = tokens.access
      state.refreshToken = tokens.refresh
    },

    setFilter(state, value) {
      state.filter = value
    }
  },

  actions: {
    setToken(context, value) {
      context.commit('setToken', value);
    },

    setJwt(context, value) {
      context.commit('setJwt', value)
    },

    setFilter(context, value) {
      context.commit('setFilter', value)
    },
  },

  modules: {
  },
  
  plugins: [createPersistedState({
    storage: {
      getItem: key => Cookies.get(key),
      setItem: (key, value) => Cookies.set(key, value, { expires: 3, secure: false }),
      removeItem: key => Cookies.remove(key)
    }
  })]
})
