<script setup>
import GradientLineChart from "@/examples/Charts/GradientLineChart.vue";
import ProjectList from "./components/ProjectsList.vue";
import { onMounted } from "vue";
import { useStore } from "vuex";

const store = useStore();

onMounted(() => {
  if (store.state.authToken && store.state.userEmail) {
    store.dispatch("fetchProjects"); // Fetch projects when the component mounts
  }
});
</script>

<template>
  <div class="row">
    <!-- Project List component -->
    <ProjectList />
    <div class="col-lg-7 mb-lg">
      <div class="card z-index-2">
        <!-- Gradient Line Chart component with props -->
        <GradientLineChart
          id="chart-line"
          title="Sales Overview"
          description="<i class='fa fa-arrow-up text-success'></i>
          <span class='font-weight-bold'>4% more</span> in 2021"
          :chart="{
            labels: [
              'Apr',
              'May',
              'Jun',
              'Jul',
              'Aug',
              'Sep',
              'Oct',
              'Nov',
              'Dec',
            ],
            datasets: [
              {
                label: 'Mobile Apps',
                data: [50, 40, 300, 220, 500, 250, 400, 230, 500],
              },
            ],
          }"
        />
      </div>
    </div>
  </div>
</template>
