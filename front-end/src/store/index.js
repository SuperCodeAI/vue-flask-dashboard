import { createStore } from "vuex";
import axios from 'axios';

export default createStore({
  state: {
    hideConfigButton: false,
    isPinned: false,
    showConfig: false,
    sidebarType: "bg-white",
    isRTL: false,
    mcolor: "",
    darkMode: false,
    isNavFixed: false,
    isAbsolute: false,
    showNavs: true,
    showSidenav: true,
    showNavbar: true,
    showFooter: true,
    showMain: true,
    layout: "default",
    authToken: localStorage.getItem('authToken') || null,
  },
  mutations: {
    toggleConfigurator(state) {
      state.showConfig = !state.showConfig;
    },
    sidebarMinimize(state) {
      let sidenav_show = document.querySelector("#app");
      if (state.isPinned) {
        sidenav_show.classList.add("g-sidenav-hidden");
        sidenav_show.classList.remove("g-sidenav-pinned");
        state.isPinned = false;
      } else {
        sidenav_show.classList.add("g-sidenav-pinned");
        sidenav_show.classList.remove("g-sidenav-hidden");
        state.isPinned = true;
      }
    },
    sidebarType(state, payload) {
      state.sidebarType = payload;
    },
    navbarFixed(state) {
      if (state.isNavFixed === false) {
        state.isNavFixed = true;
      } else {
        state.isNavFixed = false;
      }
    },
    setAuthToken(state, token) {
      state.authToken = token;
      localStorage.setItem('authToken', token);
    },
    clearAuthToken(state) {
      state.authToken = null;
      localStorage.removeItem('authToken');
    },
  },
  actions: {
    toggleSidebarColor({ commit }, payload) {
      commit("sidebarType", payload);
    },
    signin({ commit }, credentials) {
      axios.post('http://localhost:5000/api/signin', credentials)
      .then(response => {
        commit('setAuthToken', response.data.access_token);
        // Here you can also redirect the user or perform other actions upon successful login
      })
      .catch(error => {
        console.error('Signin Error:', error);
        // Handle login error (e.g., show error message)
      });      
    },
    logout({ commit }) {
      commit('clearAuthToken');
    
  },
},
  getters: {},
});
