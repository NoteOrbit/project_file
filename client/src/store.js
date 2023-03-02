
import createPersistedState from 'vuex-persistedstate'
import { createStore } from "vuex";

// const state = {
//     currentUser: "asdasd"
// }

// const actions = {
//     async getCurrentUser({ commit }) {
//         try {
//             const response = await axios.get('/protected')
//             commit('setCurrentUser', response.data.logged_in_as)
//             console.log(state.currentUser)
//         } catch (e) {
//             console.log(e)
//         }
//     }
// }

// const mutations = {
//     setCurrentUser(state, currentUser) {
//         state.currentUser = currentUser
//         localStorage.setItem('currentUser', currentUser)
//     }
// }

// const getters = {
//     currentUser: state => state.currentUser
// }

// const store = createStore({
//   state,
//   getters,
//   mutations,
//   actions,
//   plugins: [createPersistedState()]
// });

// export default store;

// import the named export from the Vuex store


// create the Vuex store using the named export

import axios from './axios';
const store = createStore({
  state: {
    access_token: localStorage.getItem('token') || null,
    token_valid: false,
    currentUser: localStorage.getItem('currentUser') || null
  },
    mutations: {
      setAccessToken(state, access_token) {
        state.access_token = access_token;
        state.token_valid = true;
      },
      clearAccessToken(state) {
        state.access_token = null;
        state.token_valid = false;
      },
      setCurrentUser(state, currentUser) {
        state.currentUser = currentUser;
        localStorage.setItem('currentUser', currentUser);
      },
    },
    actions: {
      async checkTokenValidity({ commit, state }) {
        if (!state.access_token) {
          commit('clearAccessToken');
          return false;
        }
  
        try {
          await axios.get('/protected', {
            headers: {
              Authorization: `Bearer ${state.access_token}`,
            },
          });
          return true;
        } catch (error) {
          if (error.response.status === 401 && error.response.data.msg === 'Token has expired') {
            commit('clearAccessToken');
          }
          return false;
        }
      },
      async login({ commit }, { username, password }) {
        try {
          const response = await axios.post('/login', { username, password });
          
          const access_token = response.data.access_token;
          localStorage.setItem('token', access_token);
          commit('setAccessToken', access_token);
          return true;
        } catch (error) {
          console.error(error);
          return false;
        }
      },
    },
  });
  
  export default store;