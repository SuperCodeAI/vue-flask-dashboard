<script setup>
import ProjectList from "./components/ProjectsList.vue";
import MemoryGauge from "./components/MemoryGaugeComponent.vue";
import { onMounted, onUnmounted, computed, ref} from "vue";
import { useStore } from "vuex";

const store = useStore();

const filteredNodes = computed(() => {
  const allNodes = store.getters.userNodes;
  const selectedNodeNames = store.state.selectedProjectNodeNames;
  return allNodes.filter((node) => selectedNodeNames.includes(node.name));
});


const getNodeFreeMemory = (nodeName) => {
  const selectedNodeNames = store.state.selectedProjectNodeNames;
  if (selectedNodeNames.includes(nodeName)) {
    return store.getters.getNodeMemory(nodeName) || 0;
  }
  return 0; // If the node is not part of the selected project, return 0
};

onMounted(() => {
  // 인증 토큰과 사용자 이메일이 있을 때만 프로젝트 목록을 가져옵니다.
  if (store.state.authToken && store.state.userEmail) {
    store.dispatch("fetchProjects");
    // 실시간 데이터 가져오기를 시작합니다.
    startFetchingNodeMonitoringData();
  }
});

// 컴포넌트가 언마운트될 때 데이터 가져오기를 중단합니다.
onUnmounted(() => {
  stopFetchingNodeMonitoringData();
});

// 실시간 데이터를 Store에 주기적으로 가져오기 위한 로직입니다.
const dataInterval = ref(null);

function startFetchingNodeMonitoringData() {
  stopFetchingNodeMonitoringData(); // Prevent multiple intervals
  dataInterval.value = setInterval(() => {
    store.dispatch("fetchData");
  }, 1000);
}

function stopFetchingNodeMonitoringData() {
  if (dataInterval.value) {
    clearInterval(dataInterval.value);
    dataInterval.value = null;
  }
}

</script>

<template>
  <div class="dashboard">
    <ProjectList />
    <MemoryGauge
      v-for="node in filteredNodes"
      :key="node.id"
      :nodeName="node.name"
      :total-size="node?.total_memory_mb"
      :remaining-size="getNodeFreeMemory(node.name)"
    />
    <div class="memory-info">
        Total Memory: {{ node.total_memory_mb }} MB
        <br>
        Free Memory: {{ getNodeFreeMemory(node.name) }} MB
      </div>
  </div>
</template>

<style>
.dashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
}

.node-info {
  margin-bottom: 20px;
}
.memory-info {
  margin-top: 10px;
  font-size: 16px;
  color: #333;
}
</style>
