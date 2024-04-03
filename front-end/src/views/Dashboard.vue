<script setup>
import GradientLineChart from "@/examples/Charts/GradientLineChart.vue";
</script>
<template>
  <div class="row">
    <div class="col-lg-7 mb-lg">
      <!-- line chart -->
      <div class="card z-index-2">
        <gradient-line-chart
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
