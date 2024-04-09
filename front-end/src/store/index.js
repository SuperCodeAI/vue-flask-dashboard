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
    models: [],
    datasets: [],
    projects: [], // Add a projects array to your state
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
    // 백엔드에서 모델, 데이터셋 자료 받아옴
    setModels(state, models) {
      state.models = models;
    },
    setDatasets(state, datasets) {
      state.datasets = datasets;
    },
    // 프로젝트 db에서 사용자 프로젝트 가져옴 
    setProjects(state, projects) {
      state.projects = projects;
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
    async fetchModels({ commit }) {
      try {
        const response = await axios.get(
          "http://localhost:5000/api/data/models",
        );
        commit("setModels", response.data);
      } catch (error) {
        console.error("Error fetching models:", error);
      }
    },
    async fetchDatasets({ commit }) {
      try {
        const response = await axios.get(
          "http://localhost:5000/api/data/datasets",
        );
        commit("setDatasets", response.data);
      } catch (error) {
        console.error("Error fetching datasets:", error);
      }
    },
    fetchProjects({ commit, state }) {
      axios
        .post("http://localhost:5000/api/data/projects", {
          email: state.userEmail, // send the stored email
        }, {
          headers: {
            Authorization: `Bearer ${state.authToken}`, // send the stored authToken
          },
        })
        .then((response) => {
          commit("setProjects", response.data); // commit the projects to the state
        })
        .catch((error) => {
          console.error("Error fetching projects:", error);
        });
    },
  },
  getters: {
    userProjects: (state) => state.projects, // Add a getter for the projects
  },
});
