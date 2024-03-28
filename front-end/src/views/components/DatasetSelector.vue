<template>
    <div class="dataset-selector-container">
      <h2 class="dataset-header">Dataset Selection</h2>
      <div class="dataset-content">
        <div class="dataset-list">
          <ul>
            <li v-for="dataset in datasets" :key="dataset.id" @click="selectDataset(dataset)" :class="{ selected: dataset === selectedDataset }">
              {{ dataset.name }}
            </li>
          </ul>
        </div>
        <div class="dataset-description">
          <h3>{{ selectedDataset.name }}</h3>
          <p>{{ selectedDataset.description }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const datasets = ref([
    { id: 1, name: 'Dataset A', description: 'Description of Dataset A', selected: false },
    { id: 2, name: 'Dataset B', description: 'Description of Dataset B', selected: false },
    // Continue adding datasets here
  ]);
  
  const selectedDataset = ref(datasets.value[0]); // Initialize with the first dataset
  
  const selectDataset = (dataset) => {
    datasets.value.forEach(d => d.selected = false); // Deselect all datasets
    dataset.selected = true; // Select the clicked dataset
    selectedDataset.value = dataset; // Set the selected dataset to display its details
  };
  </script>
  
  <style scoped>
  .dataset-selector-container {
    border: 1px solid #ddd;
    background-color: #fff;
    border-radius: 8px;
  }
  .dataset-header {
  text-align: left;
  padding: 10px 20px;
  background: #f5f5f5; /* Header background */
  margin: 0; /* Remove default margin */
  border-bottom: 1px solid #ddd; /* Separator */
  }

  .dataset-content {
  display: flex;
  }

  .dataset-list ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
    width: 250px;
    border-right: 1px solid #ddd;
  }
  
  .dataset-list li {
    padding: 15px 20px;
    cursor: pointer;
    border-bottom: 1px solid #eee;
    transition: background-color 0.3s;
  }
  
  .dataset-list li:hover, .dataset-list li.selected {
    background-color: #b1f397;
  }
  
  .dataset-description {
    padding: 20px;
    flex-grow: 1;
    border-radius: 0 8px 8px 0;
  }
  
  .dataset-description h3 {
    margin-top: 0;
  }
  
  @media (max-width: 768px) {
    .dataset-selector-container {
      flex-direction: column;
    }
  
    .dataset-list ul {
      width: auto;
      border-right: none;
    }
  
    .dataset-list li {
      border-bottom: none;
    }
  }
  </style>
  