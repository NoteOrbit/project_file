<template>

    <Bar v-if="loaded" :data="chartData" />

</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
import axios from '../axios.js'
export default {
  name: 'BarChart',
  components: { Bar },
  data: () => ({
    loaded: false,
    chartData: {
      labels: ['SUNDAY', 'MONDAY', 'TUESDAY', 'WENESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'],
      datasets: [
        {
          label: 'GET',
          data: Array.from({ length: 7 }, () => 0),
          borderColor: '#36A2EB',
          backgroundColor: '#9BD0F5'
        },
        {
          label: 'POST',
          data: Array.from({ length: 7 }, () => 0),
          borderColor: '#FF6384',
          backgroundColor: '#FFB1C1',
        }
      ],
      borderColor: '#36A2EB',
      backgroundColor: '#9BD0F5',
    },
    chartOptions: {
      responsive: true
    }
  }),
   async mounted() {
    this.loaded = false
    try {
      axios.get('/7day')
      .then(response => {
        let data1 = response.data;
        let getData = Array.from({ length: 7 }, () => 0);
        let postData = Array.from({ length: 7 }, () => 0);
        data1.forEach(d => {
          if (d._id.method === 'GET') {
            getData[d._id.dayOfWeek-1] = d.count;
          } else if (d._id.method === 'POST') {
            postData[d._id.dayOfWeek-1] = d.count;
          }
        });
        this.chartData.datasets[0].data = getData;
        this.chartData.datasets[1].data = postData;
        console.log(this.chartData.datasets[0].data)

        this.loaded = true
      })
    } catch (e) {
      console.error(e)
    }
  }
}
</script>


<!-- <template>
  <Bar :data="data" :options="options" />
</template>

<script lang="ts">
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  Colors
} from 'chart.js'
import { Bar } from 'vue-chartjs'
import axios from '../axios.js'
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, Colors)

export default {
  name: 'App',
  components: {
    Bar
  },
  data() {
    return {
      data: {
        labels: ['SUNDAY', 'MONDAY', 'TUESDAY', 'WENESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'],
        datasets: [
          {
            label: 'GET',
            data: Array.from({ length: 7 }, () => 0),
            borderColor: '#36A2EB',
            backgroundColor: '#9BD0F5'
          },
          {
            label: 'POST',
            data: Array.from({ length: 7 }, () => 0),
            borderColor: '#FF6384',
            backgroundColor: '#FFB1C1',
          }
        ],
        borderColor: '#36A2EB',
        backgroundColor: '#9BD0F5',
      },
      options: {
        responsive: true
      }
    }
  },
  mounted() {
    axios.get('/7day')
      .then(response => {
        let data1 = response.data;
        let getData = Array.from({ length: 7 }, () => 0);
        let postData = Array.from({ length: 7 }, () => 0);
        data1.forEach(d => {
          if (d._id.method === 'GET') {
            getData[d._id.dayOfWeek] = d.count;
          } else if (d._id.method === 'POST') {
            postData[d._id.dayOfWeek] = d.count;
          }
        });
        this.data.datasets[0].data = getData;
        this.data.datasets[1].data = postData;
        console.log(this.data.datasets[0].data)
      });
  }
}
</script> -->