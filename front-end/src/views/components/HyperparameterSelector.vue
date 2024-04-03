<template>
  <div class="hyperparameter-settings">
    <h2>Hyperparameter Settings</h2>
    <div class="hyperparameters">
      <div class="form-group">
        <label for="learningRate">Learning Rate</label>
        <input
          type="text"
          id="learningRate"
          v-model="localHyperparameters.learningRate"
          @input="handleLearningRateInput($event.target.value)"
        />
      </div>
      <div class="form-group">
        <label for="batchSize">Batch Size</label>
        <input
          type="number"
          id="batchSize"
          v-model.number="localHyperparameters.batchSize"
          @input="emitUpdate"
          min="1"
          step="1"
        />
      </div>

      <div class="form-group">
        <label for="epochs">Epochs</label>
        <input
          type="number"
          id="epochs"
          v-model.number="localHyperparameters.epochs"
          @input="emitUpdate"
          min="1"
          step="1"
        />
      </div>

      <div class="form-group">
        <label for="optimizer">Optimizer</label>
        <select id="optimizer" v-model="localHyperparameters.optimizer">
          <option value="adam">Adam</option>
          <option value="sgd">SGD</option>
          <option value="rmsprop">RMSprop</option>
        </select>
      </div>
      <div class="form-group">
        <label for="lossFunction">Loss Function</label>
        <select id="lossFunction" v-model="localHyperparameters.lossFunction">
          <option value="categorical_crossentropy">
            Categorical Crossentropy
          </option>
          <option value="sparse_categorical_crossentropy">
            Sparse Categorical Crossentropy
          </option>
          <option value="mean_squared_error">Mean Squared Error</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from "vue";

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      learningRate: "0.001",
      batchSize: "32",
      epochs: "10",
      optimizer: "adam",
      lossFunction: "categorical_crossentropy",
    }),
  },
});
const emit = defineEmits(["update:modelValue"]);

const localHyperparameters = ref({ ...props.modelValue });

const handleLearningRateInput = (value) => {
  if (value === "" || /^0\.\d*$|^\.\d+$|^0$/.test(value)) {
    localHyperparameters.value.learningRate = value;
  }
  emitUpdate();
};

watch(
  () => props.modelValue,
  (newValue) => {
    if (newValue) {
      localHyperparameters.value = { ...newValue };
    }
  },
  { deep: true },
);

const emitUpdate = () => {
  // 문자열로 변환해야 하는 필드에 대한 변환 처리
  const updatedHyperparameters = {
    ...localHyperparameters.value,
    learningRate: String(localHyperparameters.value.learningRate),
    batchSize: String(localHyperparameters.value.batchSize),
    epochs: String(localHyperparameters.value.epochs),
  };

  emit("update:modelValue", updatedHyperparameters);
};
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

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
