<template>
    <div class="hyperparameter-settings">
      <h2>Hyperparameter Settings</h2>
      <div class="hyperparameters">
        <div class="form-group">
          <label for="learningRate">Learning Rate</label>
          <input type="number" id="learningRate" v-model.number="hyperparameters.learningRate" min="0.001" step="0.0001">
        </div>
        <div class="form-group">
          <label for="batchSize">Batch Size</label>
          <input type="number" id="batchSize" v-model.number="hyperparameters.batchSize" min="1">
        </div>
        <div class="form-group">
          <label for="epochs">Epochs</label>
          <input type="number" id="epochs" v-model.number="hyperparameters.epochs" min="1">
        </div>
        <div class="form-group">
          <label for="optimizer">Optimizer</label>
          <select id="optimizer" v-model="hyperparameters.optimizer">
            <option value="adam">Adam</option>
            <option value="sgd">SGD</option>
            <option value="rmsprop">RMSprop</option>
            <!-- Add more optimizers as needed -->
          </select>
        </div>
        <div class="form-group">
          <label for="lossFunction">Loss Function</label>
          <select id="lossFunction" v-model="hyperparameters.lossFunction">
            <option value="categorical_crossentropy">Categorical Crossentropy</option>
            <option value="sparse_categorical_crossentropy">Sparse Categorical Crossentropy</option>
            <option value="mean_squared_error">Mean Squared Error</option>
            <!-- Add more loss functions as needed -->
          </select>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { reactive } from 'vue';
  
  const hyperparameters = reactive({
    learningRate: 0.001,
    batchSize: 32,
    epochs: 10,
    optimizer: 'adam',
    lossFunction: 'categorical_crossentropy',
  });
  </script>
  
  <style scoped>
  .hyperparameter-settings {
    max-width: 100%;
  }
  
  .hyperparameters {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 20px;
  }
  
  .form-group {
    flex: 1;
    min-width: 160px; /* Adjust the minimum width as needed */
  }
  
  .form-group label {
    display: block;
    margin-bottom: 5px;
  }
  
  .form-group input, .form-group select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  </style>
  