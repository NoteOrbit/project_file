<template>
  <Pie v-if='loaded' ref="myPieChart" :data="chartData" :options="chartOptions" ></Pie>
</template>

<script>
import axios from '../axios.js';
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

export default ({
  name: "Piechart",
  components: { Pie },
  data: () => ({
    chartData: {
      labels: ['View', 'Like', 'Review'],
      datasets: [
        {
          backgroundColor: [
            '#41B883',
            '#E46651',
            '#00D8FF',
          ],
          data: [0, 0, 0]
        }
      ],
    },
    loaded : false,
    chartOptions: {
      responsive: true,
      plugins: {
        tooltip: {
          callbacks: {
            label: function(context) {
              var label = context.label || '';
              if (label) {
                label += ': ';
              }
              var value = context.parsed || 0;
              var total = context.dataset.data.reduce((acc, cur) => acc + cur, 0);
              var percentage = Math.round(value / total * 100);
              label += value + ' (' + percentage + '%)';
              return label;
            },
            title: function() {
              return '';
            }
          }
        }
      }
    }
  }),
  async mounted() {
    try {
      const response = await axios.get('count_overview');
      const { values_event, values_review } = response.data;
      const viewCount = values_event.find(event => event._id === 'view');
      const likeCount = values_event.find(event => event._id === 'like');
      const reviewCount = values_review;
      this.chartData.datasets[0].data = [viewCount.count, likeCount.count, reviewCount];
      this.loaded = true
    } catch (error) {
      console.log(error);
    }
  }
})
</script>

<style>
</style>
