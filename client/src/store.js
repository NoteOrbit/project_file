import axios from './axios'
import createPersistedState from 'vuex-persistedstate'
import { createStore } from "vuex";

const state = {
    currentUser: "asdasd"
}

const actions = {
    async getCurrentUser({ commit }) {
        try {
            const response = await axios.get('/protected')
            commit('setCurrentUser', response.data.logged_in_as)
            console.log(state.currentUser)
        } catch (e) {
            console.log(e)
        }
    }
}

const mutations = {
    setCurrentUser(state, currentUser) {
        state.currentUser = currentUser
        localStorage.setItem('currentUser', currentUser)
    }
}

const getters = {
    currentUser: state => state.currentUser
}

const store = createStore({
  state,
  getters,
  mutations,
  actions,
  plugins: [createPersistedState()]
});

export default store;