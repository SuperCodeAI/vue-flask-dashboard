<script setup>
import ProjectList from "./components/ProjectsList.vue";
import { onMounted, watch, computed, onUnmounted, ref } from "vue";
import { useStore } from "vuex";

const store = useStore();
const intervalId = ref(null); // Use a ref to keep track of the interval ID

function startFetching(projectId) {
  if (intervalId.value) {
    clearInterval(intervalId.value); // Clear the current interval if it exists
  }
  intervalId.value = setInterval(() => {
    store.dispatch("fetchProjectInfoById", projectId);
  }, 3000); // Fetch every 3 seconds
}

onMounted(() => {
  if (store.state.authToken && store.state.userEmail) {
    store.dispatch("fetchProjects");
    // Assuming project ID is already selected somewhere and stored in the state
    if (store.state.selectedProjectId) {
      startFetching(store.state.selectedProjectId);
    }
  }
});

watch(() => store.state.selectedProjectId, (newId) => {
  if (newId && store.state.authToken && store.state.userEmail) {
    store.dispatch("fetchProjectInfoById", newId); // Fetch immediately when ID changes
    startFetching(newId); // Start or restart the fetching interval
  } else {
    if (intervalId.value) {
      clearInterval(intervalId.value); // Clear the interval if the ID becomes invalid
      intervalId.value = null;
    }
  }
}, { immediate: true });

onUnmounted(() => {
  // Clean up the interval when the component is destroyed
  if (intervalId.value) {
    clearInterval(intervalId.value);
  }
});

// Computed property to display project info
const projectInfo = computed(() => store.state.projectsInfo[store.state.selectedProjectId] || {});

</script>

<template>
  <div class="dashboard">
    <div class="project-list-container">
      <ProjectList />
    </div>
    <div class="project-info-widget" v-if="projectInfo">
    <div class="tarining-status-header">
    <h4>학습 상태</h4>
    </div>
    <p> </p> 
    <p> </p> 
    <p> </p> 
    <p class="project-info-highlight">모델 학습 진행율: {{ projectInfo.progress ? `${projectInfo.progress}%` : '0' }}</p>
    <p class="project-info-highlight epoch">모델 훈련 횟수: {{ projectInfo.epoch !== undefined ? projectInfo.epoch : '0' }}</p>
    <p class="project-info-highlight accuracy">모델 정확도: {{ projectInfo.accuracy ? projectInfo.accuracy.toFixed(2) + '%' : '0' }}</p>
    <p class="project-info-highlight loss">모델 Loss 값: {{ projectInfo.loss ? projectInfo.loss.toFixed(4) : '0' }}</p>

   
  </div>
  </div>
</template>

<style>
.dashboard {
  display: flex;
  align-items: flex-start; /* 요소들을 컨테이너의 상단에 정렬 */
  justify-content: flex-start; /* 요소들을 컨테이너의 왼쪽에서 시작하도록 정렬 */
  gap: 20px; /* 요소들 사이의 간격 */
  padding: 20px; /* 대시보드 패딩 */
  
}


.project-list-container {
  min-width: 800px; /* 최소 너비 설정 */
  max-height: 500px; /* 최대 높이 설정 */
  height: 275px; /* 높이 100%로 설정 */

}

.project-info-widget {
  flex: 1; /* 유연하게 너비 조정 */
  flex-grow: 2; /* 컨테이너가 더 많은 공간을 차지하도록 설정 */
  padding: 20px; 
  margin-top: 0; /* 위쪽 마진 제거 */
  border: 1px solid #ccc; /* 테두리 설정 */
  border-radius: 12px;
  background-color: #fff;
  box-shadow: 0 25px 30px rgba(0, 0, 0, 0.07);
  height: 310px;
}


/* 헤더 스타일 */
h4 {
  margin-bottom: 20px; /* 여백을 더 줍니다 */
  font-size: 22px; /* 크기를 키웁니다 */
  font-weight: 600; /* 조금 더 강조된 두께 */
  color: #333; /* 색상은 약간 어두운 회색으로 조정 */
}

/* 단락 스타일 */
p {
  font-size: 18px; /* 텍스트 크기를 키웁니다 */
  color: #666; /* 색상은 좀 더 연한 회색으로 조정 */
  margin-bottom: 10px; /* 단락 사이의 여백을 조정 */
  line-height: 1.4; /* 줄 간격을 조정하여 가독성을 높입니다 */
}


.project-info-highlight {
  font-size: 20px; /* 크기 변경 */
  font-weight: 500; /* 더 강조된 폰트 두께 */
  font-weight: bold; /* 볼드체로 변경 */
  color: #1a237e; /* 진한 파란색으로 변경 */
}

.progress {
  font-size: 20px; /* 크기 변경 */
  font-weight: bold; /* 볼드체로 변경 */
  color: #4caf50; /* 진한 녹색으로 변경 */
}

.epoch {
  font-size: 20px; /* 크기 변경 */
  font-weight: bold; /* 볼드체로 변경 */
  color: #ff9800; /* 주황색으로 변경 */
}

.accuracy {
  font-size: 20px; /* 크기 변경 */
  font-weight: bold; /* 볼드체로 변경 */
  color: #009688; /* 테일 그린색으로 변경 */
}

.loss {
  font-size: 20px; /* 크기 변경 */
  font-weight: bold; /* 볼드체로 변경 */
  color: #f44336; /* 빨간색으로 변경 */
}


</style>
