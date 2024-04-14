<script setup>
import ProjectList from "./components/ProjectsList.vue";
import MemoryGauge from "./components/MemoryGaugeComponent.vue";
import DiskGauge from "./components/DiskGaugeComponent.vue";
import { onMounted, onUnmounted, computed, ref} from "vue";
import { useStore } from "vuex";

const store = useStore();

const filteredNodes = computed(() => {
  const allNodes = store.getters.userNodes;
  const selectedNodeNames = store.state.selectedProjectNodeNames;
  console.log("선택된 리스트의 노드 스팩 정보 가져오는 중 ")
  console.log(allNodes.filter((node) => selectedNodeNames.includes(node.name)))
  return allNodes.filter((node) => selectedNodeNames.includes(node.name));
});

// 남은 메모리 정보를 저장하는 객체
const nodeFreeMemories = computed(() => {
  const memories = {};
  filteredNodes.value.forEach(node => {
    // 여기에서 각 노드의 메모리 정보를 메모리 객체에 저장하고 바로 로그를 출력
    const memory = store.getters.getNodeMemory(node.name) || 0;
    memories[node.name] = memory;
    console.log("남은 메모리 가져오는 중: ", node.name, memory);
  });
  return memories;
});

const nodeFreeDisk = computed(() => {
  const Disks = {};
  filteredNodes.value.forEach(node => {
    // 여기에서 각 노드의 디스크 정보를 메모리 객체에 저장하고 바로 로그를 출력
    const Disk = store.getters.getNodeDisk(node.name) || 0;
    Disks[node.name] = Disk;
    console.log("남은 디스크가져오는 중: ", node.name, Disk);
  });
  return Disks;
});

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
    <div class="project-list-container">
      <ProjectList />
    </div>
    <!-- Memory Usage Section -->
    <div v-if="filteredNodes.length > 0">
      <h2 class="memory-gauge-header">메모리 사용량</h2>
      <div class="memory-gauge-wrapper">
        <div
          class="memory-gauge-container"
          v-for="node in filteredNodes"
          :key="node.id"
        >
          <MemoryGauge
            :nodeName="node.name"
            :total-size="node.total_memory_mb"
            :remaining-size="nodeFreeMemories[node.name]"
          />
        </div>
      </div>
    </div>
    <!-- Disk Usage Section -->
    <div v-if="filteredNodes.length > 0">
      <h2 class="disk-gauge-header">디스크 사용량</h2>
      <div class="disk-gauge-wrapper">
        <div
          class="disk-gauge-container"
          v-for="node in filteredNodes"
          :key="node.id"
        >
          <DiskGauge
            :nodeName="node.name"
            :total-size="node.total_disk_mb" 
            :remaining-size="nodeFreeDisk[node.name]"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.dashboard {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 20px;
  padding: 20px;
}

.project-list-container {
  flex-basis: 100%;
  max-width: 100%;
}

.memory-gauge-header {
  width: 100%; /* Ensures the header spans the full width */
  text-align: center; /* Center the text */
  margin-top: 0;
  margin-bottom: 20px; /* Space before the gauges */
}

.memory-gauge-wrapper {
  display: flex;
  flex-wrap: wrap; /* Allows gauge containers to wrap */
  width: 100%; /* Takes full width */
}

.memory-gauge-container {
  flex: 1;
  min-width: calc(50% - 30px); /* Minimum width for MemoryGauge components, accounting for the gap */
  max-width: calc(50% - 30px); /* Maximum width for MemoryGauge components, accounting for the gap */
}

.disk-gauge-header {
  width: 100%; /* Ensures the header spans the full width */
  text-align: center; /* Center the text */
  margin-top: 0;
  margin-bottom: 20px; /* Space before the gauges */
}

.disk-gauge-wrapper {
  display: flex;
  flex-wrap: wrap; /* Allows gauge containers to wrap */
  width: 100%; /* Takes full width */
}

.disk-gauge-container {
  flex: 1;
  min-width: calc(50% - 30px); /* Minimum width for MemoryGauge components, accounting for the gap */
  max-width: calc(50% - 30px); /* Maximum width for MemoryGauge components, accounting for the gap */
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