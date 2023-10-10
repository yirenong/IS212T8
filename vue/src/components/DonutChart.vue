<template>
  <canvas ref="doughnutChart" class="w-50 h-50"></canvas>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  props: {
    percentage: {
      type: Number,
      required: true
    }
  },
  mounted() {
    this.createDoughnutChart();
  },
  methods: {
    createDoughnutChart() {
      const ctx = this.$refs.doughnutChart.getContext('2d');

      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Matched', 'Not Matched'],
          datasets: [{
            data: [this.percentage, 100 - this.percentage],
            backgroundColor: ['green', 'lightgray'],
          }],
        },
        options: {
          cutout: '50%',
          responsive: true,
          legend: {
            display: false,
          },
          tooltips: {
            enabled: false,
          },
        },
      });
    }
  }
};
</script>
  