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
      <h4>Project Info</h4>
      <p>Progress: {{ projectInfo.progress ? `${projectInfo.progress}%` : 'N/A' }}</p>
      <p>Estimated Time Remaining: {{ projectInfo.eta !== undefined ? `${projectInfo.eta} seconds` : 'N/A' }}</p>
      <p>Current Epoch: {{ projectInfo.epoch !== undefined ? projectInfo.epoch : 'N/A' }}</p>
      <p>Current Batch: {{ projectInfo.batch !== undefined ? projectInfo.batch : 'N/A' }}</p>
      <p>Current Accuracy: {{ projectInfo.accuracy ? projectInfo.accuracy.toFixed(2) + '%' : 'N/A' }}</p>
      <p>Current Loss: {{ projectInfo.loss ? projectInfo.loss.toFixed(4) : 'N/A' }}</p>
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

.project-info-widget {
  width: 300px; /* Set the width as needed */
  padding: 20px;
  margin-top: 20px; /* Spacing from the top element */
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

</style>
