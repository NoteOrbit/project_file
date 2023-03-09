<template>
  
  <div class="row justify-center q-gutter-sm">
    <div class="col-12 col-md-auto" v-for="item in data.data" :key="item._id">
    <q-card class="my-card bg-black text-white" >

        <q-card-section>
          <h5>{{ item._id }}</h5>
          <h6>NUMBER {{ item._id }} {{ item.count }}</h6>
        </q-card-section>

    </q-card>
    </div>
  </div>

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