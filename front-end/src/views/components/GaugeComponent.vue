<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps } from "vue";
import Chart from "chart.js/auto";

const props = defineProps({
  totalSize: Number,
  remainingSize: Number,
  nodeName: String
});

const chartCanvas = ref(null);
let myChart = null;

// Chart.js chart configuration
const config = {
  type: "doughnut",
  data: {
    labels: ["Used", "Free"],
    datasets: [
      {
        data: [0, 0], // Initial dummy data
        backgroundColor: ["#42A5F5", "#ddd"],
        borderWidth: 0,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      animateRotate: true,
      animateScale: false,
    },
    circumference: 180,
    rotation: 270,
  },
};

onMounted(() => {
  if (!chartCanvas.value) {
    console.error("Canvas element not found");
    return;
  }
  const context = chartCanvas.value.getContext('2d');
  if (!context) {
    console.error("Failed to get canvas context");
    return;
  }
  myChart = new Chart(context, config);
});

watch(
  [() => props.totalSize, () => props.remainingSize],
  (newValues) => {
    console.log("New values received:", newValues);
    const [totalSize, remainingSize] = newValues;
    const usedSize = totalSize - remainingSize;
    if (myChart) {
      myChart.data.datasets[0].data = [usedSize, remainingSize];
      myChart.update();
    }
  },
  { immediate: true }
);
</script>

<style>
.chart-container {
  overflow: visible; /* Ensures no clipping */
  opacity: 1; /* Checks that it's not hidden */
  position: relative;
  height: 40vh;
  width: 80vw;
}
</style>
