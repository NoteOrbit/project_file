<template>


        <Line v-if="loaded" :data="chartData" :options="chartOptions" />


</template>

<script>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)
import axios from '../axios.js'
export default {
  name: 'LineChart',
  components: { Line },
  data: () => ({
    loaded: false,
    chartData: {
      labels: ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'],
      datasets: [
        {
          label: 'GET',
          data: Array.from({ length: 7 }, () => 0),
          borderColor: '#36A2EB',
          backgroundColor: '#9BD0F5',
          fill: false
        },
        {
          label: 'POST',
          data: Array.from({ length: 7 }, () => 0),
          borderColor: '#FF6384',
          backgroundColor: '#FFB1C1',
          fill: false
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
              getData[d._id.dayOfWeek - 1] = d.count;
            } else if (d._id.method === 'POST') {
              postData[d._id.dayOfWeek - 1] = d.count;
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

<style>

.pie-container {

  width: 1000px;
  height: 1000px;

}
</style>