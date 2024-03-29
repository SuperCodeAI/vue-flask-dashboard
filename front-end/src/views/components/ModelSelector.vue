<template>
  <div class="model-selector-container">
    <!-- Header title for the model selection -->
    <h2 class="model-header">Model Selection</h2>
    <!-- Model list and description container -->
    <div class="model-content">
      <div class="model-list">
        <ul>
          <li
            v-for="model in models"
            :key="model.id"
            @click="updateSelectedModel(model)"
            :class="{ selected: model === selectedModel }"
          >
            {{ model.name }}
          </li>
        </ul>
      </div>
      <div class="model-description">
        <h3>{{ selectedModel?.name }}</h3>
        <p>{{ selectedModel?.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, watch, defineEmits } from "vue";

const props = defineProps({
  modelValue: Object,
});

const emit = defineEmits(["update:modelValue"]);

const models = ref([
  { id: 1, name: "Model A", description: "This is a description of Model A." },
  { id: 2, name: "Model B", description: "This is a description of Model B." },
  { id: 3, name: "Model C", description: "This is a description of Model C." },
  // Continue adding models here
]);

const selectedModel = ref(props.modelValue || models.value[0]);

// Watches for changes to props.modelValue
watch(
  () => props.modelValue,
  (newValue) => {
    selectedModel.value = newValue;
  },
);

const updateSelectedModel = (model) => {
  selectedModel.value = model;
  // Emit event for v-model to work
  emit("update:modelValue", model);
};
</script>

<style scoped>
.model-selector-container {
  border: 1px solid #ddd;
  background-color: #fff; /* Set background to white */
  border-radius: 8px; /* 모서리 둥글게  */
  flex-direction: column;
}
.model-header {
  text-align: left;
  padding: 10px 20px;
  background: #ececec;
  margin: 0;
  border-bottom: 1px solid #ddd;
}

.model-content {
  display: flex;
}

.model-list ul {
  list-style-type: none; /* Removes the default list styling */
  padding: 0;
  margin: 0;
  width: 250px; /* Set the width of the list */
  border-right: 1px solid #ddd;
}

.model-list li {
  padding: 15px 20px; /* Provide padding to each list item */
  cursor: pointer;
  border-bottom: 1px solid #eee; /* Add separation between items */
  transition: background-color 0.3s; /* Smooth transition for background color */
  font-size: 18px; /*폰트 사이즈 조절*/
}

.model-list li:hover,
.model-list li.selected {
  background-color: #b1f397; /* A light grey background for hover state */
}

.model-description {
  padding: 20px; /* Give some padding around the description */
  flex-grow: 1; /* Ensure it fills the remaining space */
  border-radius: 0 8px 8px 0; /* Rounded corners on the right side */
}

.model-description h3 {
  margin-top: 0; /* Remove default margin from the heading */
}

/* Optional: Add some responsive styling */
@media (max-width: 768px) {
  .model-selector-container {
    flex-direction: column; /* Stack list and description on smaller screens */
  }

  .model-list ul {
    width: auto; /* List takes full width on smaller screens */
    border-right: none;
  }

  .model-list li {
    border-bottom: none; /* Remove border when in column layout */
  }
}
</style>
