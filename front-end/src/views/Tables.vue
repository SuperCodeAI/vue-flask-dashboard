<script setup>
import { reactive, ref } from 'vue';
import ModelselectBox from "./components/ModelSelector.vue";
import DatasetselectBox from "./components/DatasetSelector.vue";
import HyperparameterselectBox from "./components/HyperparameterSelector.vue";
import NodeselectBox from "./components/NodeSelector.vue";
import axios from 'axios';

// Reactive state to store selections
const projectData = reactive({
  model: "", // Assuming model is a string
  dataset: "", // Assuming dataset is a string
  hyperparameters: {
    learningRate: 0.001,
    batchSize: 64,
    epochs: 100,
    optimizer: "Adam",
    lossFunction: "CrossEntropyLoss"
  },
  nodes: [] // Assuming nodes is an array of strings
});


const isCreatingProject = ref(false);

// Method to send data to backend
const createProject = async () => {
  try {
    isCreatingProject.value = true;
    const response = await axios.post('/api/create-project', projectData);
    console.log(response.data);
    // Handle successful project creation (e.g., redirect or show message)
  } catch (error) {
    console.error('Failed to create project:', error);
    // Handle errors (e.g., show error message)
  } finally {
    isCreatingProject.value = false;
  }
};


</script>
<template>
  <div class="py-5 container-fluid">
    <div class="row">
      <div class="col-12">
        <ModelselectBox />
      </div>
    </div>
  </div>
  <div class="py-2 container-fluid">
    <div class="row">
      <div class="col-12">
        <DatasetselectBox />
      </div>
    </div>
  </div>
  <div class="py-2 container-fluid">
    <div class="row">
      <div class="col-12">
        <HyperparameterselectBox />
      </div>
    </div>
  </div>

  <div class="py-2 container-fluid">
    <div class="row">
      <div class="col-12">
        <NodeselectBox />
      </div>
    </div>

    <button @click="createProject" :disabled="isCreatingProject">
      {{ isCreatingProject ? 'Creating...' : 'Create Project' }}
    </button>
  </div>

  <!-- ... other parts of the template ... -->
  <ModelselectBox v-model="projectData.model" />
  <DatasetselectBox v-model="projectData.dataset" />
  <HyperparameterselectBox v-model="projectData.hyperparameters.learningRate" prop="learningRate" />
  <HyperparameterselectBox v-model="projectData.hyperparameters.batchSize" prop="batchSize" />
  <HyperparameterselectBox v-model="projectData.hyperparameters.epochs" prop="epochs" />
  <HyperparameterselectBox v-model="projectData.hyperparameters.optimizer" prop="optimizer" />
  <HyperparameterselectBox v-model="projectData.hyperparameters.llossFunction" prop="lossFunction" />
  <!-- You'll do similar for batchSize, epochs, optimizer, and lossFunction -->
  <NodeselectBox v-model="projectData.nodes" />
  <!-- ... rest of the template ... -->


</template>
