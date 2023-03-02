<template>
    <Pie  v-if ='loaded' ref="myPieChart" :data="chartData" ></Pie>
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
        chartOptions: {
        responsive: true
      }
      },
      loaded : false
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
  