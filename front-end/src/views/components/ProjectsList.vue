<template>
  <div class="project-widget">
    <h4 class="project-widget-header">Project List</h4>
    <div class="project-widget-body">
      <div class="project-list-container">
        <ul class="project-list">
          <li
            v-for="(project, index) in projects"
            :key="index"
            @click="selectProject(project)"
            :class="{ 'is-selected': project.id === selectedProject.id }"
          >
            {{ project.model_name }} - {{ project.dataset_name }}
          </li>
        </ul>
      </div>
      <div class="project-description-container">
        <h4>{{ selectedProject.model_name || "No project selected" }}</h4>
        <p>{{ selectedProject.dataset_name }}</p>
        <p>Status: {{ selectedProject.status }}</p>
        <p>Created At: {{ selectedProject.created_at }}</p>
      </div>
      <div class="project-actions-container">
        <button
          v-if="selectedProject.status === '학습 중'"
          @click="stopTraining(selectedProject.id)"
        >
          학습 중단
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { useStore } from "vuex";
import axios from "axios";

const store = useStore();
const projects = computed(() => store.getters.userProjects);
const selectedProject = ref({});

const selectProject = (project) => {
  selectedProject.value = project;
};

const stopTraining = async () => {
  if (!selectedProject.value || !selectedProject.value.id) {
    console.error(
      "No project selected or selected project does not have an id",
    );
    return;
  }
  try {
    const response = await axios.post(
      "http://localhost:5000/api/stop-training",
      {
        projectId: selectedProject.value.id, // Send the selected project's ID to the backend
      },
      {
        headers: {
          Authorization: `Bearer ${store.state.authToken}`,
        },
      },
    );
    if (response.data.success) {
      console.log("학습 중단 요청 성공", selectedProject.value.id);
      // 요청 성공 후 필요한 상태 업데이트 로직 추가
      // Here you could update the status in the `projects` array or trigger a re-fetch, for example
    }
  } catch (error) {
    console.error("학습 중단 요청 실패", selectedProject.value.id, error);
  }
};
</script>

<style scoped>
.project-widget {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  background-color: #fff;
  margin: 0 auto; /* Center the widget */
  margin-bottom: 20px; /* Add bottom margin */
  width: calc(100% - 10px); /* Reduce the total width by 20px from each side */
  max-width: 1200px; /* Optionally add a max-width if you want to limit the size on larger screens */
}

.project-widget-header {
  background-color: #f9f9f9;
  padding: 12px 16px;
  margin: 0;
  border-bottom: 1px solid #ddd;
}

.project-widget-body {
  display: flex;
}

.project-list-container {
  border-right: 1px solid #ddd;
  flex: 1;
}

.project-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.project-list li {
  padding: 8px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.project-list li:hover,
.project-list li.is-selected {
  background-color: #e8f0f9;
}

.project-description-container {
  flex: 2;
  padding: 16px;
}

.project-actions-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px;
}

button {
  border-radius: 5px; /* Adjust the pixel value to control the roundness */
  background-color: #90ee90; /* This is a light green color */
  border: none; /* Removes the default border */
  padding: 10px 20px; /* Adds some padding inside the button */
  color: rgb(0, 0, 0); /* Changes the text color to white */
  font-size: 16px; /* Adjust the font size as needed */
  cursor: pointer; /* Changes the cursor to a pointer when hovering over the button */
  transition: background-color 0.3s; /* Smooth transition for background color */
}

button:hover {
  background-color: #76c893; /* Slightly darker green color for the hover state */
}
</style>
