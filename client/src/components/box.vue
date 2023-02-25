<template>
  

  <q-row class="row justify  q-gutter-sm flex flex-center">
    
    <q-card class="my-card bg-indigo-3 text-white" v-for="item in data.data" :key="item._id"  style="width: 500px">

        <q-card-section>
          <h5>{{ item._id }}</h5>
          <h6>NUMBER {{ item._id }} {{ item.count }}</h6>
        </q-card-section>

    </q-card>
  </q-row>
  
</template>
<script>
import axios from '../axios.js';

export default {
  name: "box",
  data() {
    return {
      data: []
    }
  },
  created() {
    axios.get('logbox')
      .then(response => {
        this.data = response.data

      })
      .catch(error => {
        console.log(error)
      })
  }
}
</script>