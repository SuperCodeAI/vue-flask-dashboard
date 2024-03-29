<script setup>
import { reactive, ref } from "vue";
import ModelselectBox from "./components/ModelSelector.vue";
import DatasetselectBox from "./components/DatasetSelector.vue";
import HyperparameterselectBox from "./components/HyperparameterSelector.vue";
import NodeselectBox from "./components/NodeSelector.vue";
import axios from "axios";

const projectData = reactive({
  model: {}, // Initially an object, later to be just a string of model name
  dataset: {}, // Initially an object, later to be just a string of dataset name
  hyperparameters: {}, // Already in the desired format
  nodes: [], // Initially an array of objects, later to be an array of node names
});

const isCreatingProject = ref(false);

const prepareDataForSubmission = () => {
  return {
    model: projectData.model.name, // Just send the model name
    dataset: projectData.dataset.name, // Just send the dataset name
    hyperparameters: projectData.hyperparameters, // Already in the correct format
    nodes: projectData.nodes.map((node) => node.name), // Convert nodes array to an array of names
  };
};

// Method to send data to backend
const createProject = async () => {
  try {
    isCreatingProject.value = true;
    const formattedData = prepareDataForSubmission(); // 전달 데이터 형식 변경
    const response = await axios.post(
      "http://localhost:5000/api/create-project",
      formattedData,
    );
    console.log(response.data);
    // Handle successful project creation (e.g., redirect or show message)
  } catch (error) {
    console.error("Failed to create project:", error);
    // Handle errors (e.g., show error message)
  } finally {
    isCreatingProject.value = false;
  }
};
</script>
<template>
  <div class="container-fluid">
    <div class="py-5 container-fluid">
      <div class="row">
        <div class="col-12">
          <ModelselectBox v-model="projectData.model" />
        </div>
      </div>
    </div>

    <div class="py-2 container-fluid">
      <div class="row">
        <div class="col-12">
          <DatasetselectBox v-model="projectData.dataset" />
        </div>
      </div>
    </div>

    <div class="py-2 container-fluid">
      <div class="row">
        <div class="col-12">
          <HyperparameterselectBox v-model="projectData.hyperparameters" />
        </div>
      </div>
    </div>

    <div class="py-2 container-fluid">
      <div class="row">
        <div class="col-12">
          <NodeselectBox v-model="projectData.nodes" />
        </div>
      </div>
    </div>

    <div class="create-project-button-container">
      <button
        class="create-project-button"
        @click="createProject"
        :disabled="isCreatingProject"
      >
        {{ isCreatingProject ? "Creating..." : "Create Project" }}
      </button>
    </div>
  </div>
</template>

<style scoped>
/* ... other styles ... */

/* Add padding to the bottom of the container to push the footer down */
.container-fluid {
  padding-bottom: 50px; /* Adjust the value as needed to create space above the footer */
}

/* Adjust the styling of the button and its container */
.create-project-button-container {
  text-align: right; /* Aligns the button to the right */
  padding-top: 20px; /* Adds space above the button */
  padding-bottom: 20px; /* Adds space below the button, above the footer */
}

.create-project-button {
  padding: 10px 30px; /* Larger padding for a larger button */
  margin-top: 20px; /* Adds space above the button */
  margin-bottom: 40px; /* Adds space below the button */
  /* Other styling remains unchanged */
}

/* ... */
</style>
