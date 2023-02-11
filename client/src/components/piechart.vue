<template>
    <q-card class="q-ma-xl">
        <q-card-section>

            <Pie :data="pieData"></Pie>

        </q-card-section>
    </q-card>
</template>

<script lang="ts">
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

export default ({
    name: "Piechart",
    components: { Pie },
    data: () => ({
        pieData: {
            labels: ['VueJs', 'EmberJs', 'ReactJs', 'AngularJs'],
            datasets: [
                {
                    backgroundColor: [
                        '#41B883',
                        '#E46651',
                        '#00D8FF',
                        '#DD1B16'
                    ],
                    data: [40, 20, 80, 10]
                }
            ]
        }
    })
})
</script>
<style>

</style>
