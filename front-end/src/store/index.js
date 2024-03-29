import { createStore } from "vuex";
import axios from "axios";

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
    authToken: sessionStorage.getItem("authToken") || null,
    userEmail: sessionStorage.getItem("userEmail") || null, // 변경: 초기 상태 설정
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
      sessionStorage.setItem("authToken", token);
    },
    setUserEmail(state, email) {
      state.userEmail = email;
      sessionStorage.setItem("userEmail", email); // 변경: 이메일 세션 스토리지에 저장
    },
    clearAuthToken(state) {
      state.authToken = null;
      state.userEmail = null;
      sessionStorage.removeItem("authToken");
      sessionStorage.removeItem("userEmail"); // 변경: 이메일 세션 스토리지에서 삭제
    },
  },
  actions: {
    toggleSidebarColor({ commit }, payload) {
      commit("sidebarType", payload);
    },
    signin({ commit }, credentials) {
      return new Promise((resolve, reject) => {
        axios
          .post("http://localhost:5000/api/signin", credentials)
          .then((response) => {
            commit("setAuthToken", response.data.access_token);
            commit("setUserEmail", response.data.email); // 이메일 저장
            resolve(); // Resolve the promise indicating success
          })
          .catch((error) => {
            console.error("Signin Error:", error);
            reject(error); // Reject the promise indicating failure
          });
      });
    },
    logout({ commit }) {
      commit("clearAuthToken");
    },
  },
  getters: {},
});
