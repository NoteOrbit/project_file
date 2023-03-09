<template >
    <div>
        <q-row class="row justify q-gutter-sm ">

            <q-card class="my-card bg-black text-white" style="width: 300px">

                <q-card-section>
                    <h5 class="flex flex-center">Recommendations Item</h5>
                    <h2 class="flex flex-center">{{ data.values }}</h2>
                </q-card-section>


            </q-card>

            <q-card class="my-card bg-light-blue-8 text-white" style="width: 300px">
                
                <q-card-section>
                    <h5 class="flex flex-center">Precision@k</h5>
                    <h2 class="flex flex-center">{{ data.values }}</h2>
                </q-card-section>


            </q-card>



        </q-row>
    </div>
</template>
<script>
import axios from '../axios.js';

export default {
    name: "box_count",
    data() {
        return {
            data: []
        }
    },
    created() {

        axios.get('count_overview')
            .then(response => {
                this.data = response.data
                console.log(this.data)

            })
            .catch(error => {
                console.log(error)
            })
    }
}
</script>