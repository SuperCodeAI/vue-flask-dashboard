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
              {{ project.model_name }} - {{ project.dataset_name }} ({{ project.status }})
            </li>
          </ul>
        </div>
        <div class="project-description-container">
          <h4>{{ selectedProject.model_name || 'No project selected' }}</h4>
          <p>{{ selectedProject.dataset_name }}</p>
          <p>Status: {{ selectedProject.status }}</p>
          <p>Created At: {{ selectedProject.created_at }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed, ref } from 'vue';
  import { useStore } from 'vuex';
  
  const store = useStore();
  const projects = computed(() => store.getters.userProjects);
  const selectedProject = ref({});
  
  const selectProject = (project) => {
    selectedProject.value = project;
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
</style>