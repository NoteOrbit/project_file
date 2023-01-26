<template >
    <div>
        <div class="container-lg my-2">
              <div class="row">
    <div class="col-sm-4 p-2" v-for="item in data.data" :key="item._id">
      <div class="p-3 bg-dark text-light rounded">
      <h1>{{ item._id }}</h1>
      <h6>NUMBER {{ item._id }} {{ item.count }}</h6>
      </div>
    </div>
  </div>
  </div>
    </div>
</template>
<script>
import axios from '../axios.js';

export default {
  name : "box",
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