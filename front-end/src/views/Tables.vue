<script setup>
import { reactive, ref, computed, watch } from "vue";
import { useStore } from "vuex";
import ModelselectBox from "./components/ModelSelector.vue";
import DatasetselectBox from "./components/DatasetSelector.vue";
import HyperparameterselectBox from "./components/HyperparameterSelector.vue";
import NodeselectBox from "./components/NodeSelector.vue";
import axios from "axios";

const store = useStore();

const authToken = computed(() => store.state.authToken);

const projectData = reactive({
  model: {}, // Initially an object, later to be just a string of model_id
  dataset: {}, // Initially an object, later to be just a string of dataset_id
  hyperparameters: {}, // Already in the desired format
  nodes: [], // Initially an array of objects, later to be an array of node names
});

const isCreatingProject = ref(false);

watch(
  projectData.hyperparameters,
  (newVal) => {
    console.log("Hyperparameters updated:", newVal);
  },
  { deep: true },
);

// const handleSelectedNodeChange = (selectedNode) => {
//   const index = projectData.nodes.findIndex(node => node.id === selectedNode.id);
//   if (index > -1) {
//     // Node is already selected, remove it
//     projectData.nodes.splice(index, 1);
//   } else {
//     // Node is not selected, add it
//     projectData.nodes.push(selectedNode);
//   }
// };

const prepareDataForSubmission = () => {
  return {
    model: projectData.model.model_id,
    dataset: projectData.dataset.dataset_id,
    hyperparameters: {
      ...projectData.hyperparameters,
      optimizer: projectData.hyperparameters.optimizer,
      lossFunction: projectData.hyperparameters.lossFunction,
    },
    nodes: projectData.nodes.map((node) => node.name),
  };
};

const hyperparametersSelected = (newHyperparameters) => {
  projectData.hyperparameters = {
    ...projectData.hyperparameters,
    ...newHyperparameters,
  };
};

// Method to send data to backend
const createProject = async () => {
  try {
    isCreatingProject.value = true;
    const formattedData = prepareDataForSubmission(); // 전달 데이터 형식 변경
    lastSubmittedData.value = formattedData;
    const config = {
      headers: {
        Authorization: `Bearer ${authToken.value}`,
      },
    };

    const response = await axios.post(
      "http://localhost:5000/api/create-project",
      formattedData,
      config,
    );
    // 프로젝트 생성이 성공했다면, 노드 정보 업데이트
    if (response && response.status === 200) {
      console.log("Project created successfully:", response.data);
      // 프로젝트 생성 후 노드 정보 새로고침
      await store.dispatch("fetchNodes");
      // 성공 메시지 처리 또는 사용자 인터페이스 업데이트 등의 추가적인 처리를 여기에 추가할 수 있습니다.
    }
    console.log(response.data);
    // Handle successful project creation (e.g., redirect or show message)
  } catch (error) {
    console.error("Failed to create project:", error);
    // Handle errors (e.g., show error message)
  } finally {
    isCreatingProject.value = false;
  }
};

const modelIdSelected = (modelId) => {
  if (modelId) {
    const fullModel = store.state.models.find(
      (model) => model.model_id === modelId,
    );
    if (fullModel) {
      projectData.model = fullModel; // Assign the full model object
    } else {
      console.error("Model not found!");
    }
  }
};

const datasetSelected = (datasetId) => {
  projectData.dataset = { dataset_id: datasetId };
};

const stringifyData = (value) => {
  return JSON.stringify(value, null, 2); // Pretty print JSON
};

const lastSubmittedData = ref(null); // 백엔드로 마지막으로 전송된 데이터를 저장
</script>

<template>
  <div class="container-fluid">
    <div class="py-5 container-fluid">
      <div class="row">
        <div class="col-12">
          <ModelselectBox @update:modelValue="modelIdSelected" />
        </div>
      </div>
    </div>

    <div class="py-2 container-fluid">
      <div class="row">
        <div class="col-12">
          <DatasetselectBox @update:modelValue="datasetSelected" />
        </div>
      </div>
    </div>

    <div class="py-2 container-fluid">
      <div class="row">
        <div class="col-12">
          <HyperparameterselectBox
            @update:modelValue="hyperparametersSelected"
          />
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
    <div class="last-submitted-data-container">
      <h3>Last Submitted Data</h3>
      <pre>{{ stringifyData(lastSubmittedData) }}</pre>
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

.last-submitted-data-container {
  margin-top: 20px;
  background-color: #fbfafa;
  padding: 15px;
  border-radius: 5px;
}

button {
  border-radius: 5px; /* Adjust the pixel value to control the roundness */
  background-color: #90ee90; /* This is a light green color */
  border: none; /* Removes the default border */
  padding: 10px 20px; /* Adds some padding inside the button */
  color: rgb(0, 0, 0); /* Changes the text color */
  font-size: 16px; /* Adjust the font size as needed */
  cursor: pointer; /* Changes the cursor to a pointer when hovering over the button */
  transition: background-color 0.3s; /* Smooth transition for background color */
}

button:hover {
  background-color: #76c893; /* Slightly darker green color for the hover state */
}
/* ... */
</style>
