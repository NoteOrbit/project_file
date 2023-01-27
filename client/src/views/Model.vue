<template lang="">
<div>
  <div class="toast-container top-0 end-0 p-3">

<!-- Then put toasts within -->
<div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
  <div class="toast-header">
    <span class="material-icons">update</span>
    <strong class="me-auto">Notifications</strong>
    <small class="text-muted">just now</small>
    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
  </div>
  <div class="toast-body">
    {{check}}
  </div>
</div>

</div>
</div>
<div class="container-lg my-5">
  <h1>Apiori</h1>
  <div class="row">
    <div class="col-sm-4 p-2">
      <div class="p-3 bg-primary text-light rounded"><h1>correct </h1><span>1>>100</span></div>
    </div>
    <div class="col-sm-4 p-2">
      <div class="p-3 bg-warning text-light rounded"><h1>item </h1><span>2>>200</span></div>
    </div>
    <div class="col-sm-4 p-2">
      <div class="p-3 bg-danger text-light rounded"><h1>Recom </h1><span>3>>300</span></div>
    </div>
  </div>
  <hr class="mt-10 mb-1"/>
  <h1 class="my-3">Model Versions</h1>
  <!-- <div>
    <div class="dropdown">
    <button
      class="btn btn-secondary dropdown-toggle"
      type="button"
      id="dropdownMenuButton1"
      data-bs-toggle="dropdown"
      aria-expanded="false"
    >
      Check Bootstrap
    </button>
    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
      <li><a class="dropdown-item" href="#">Action</a></li>
      <li><a class="dropdown-item" href="#">Another action</a></li>
      <li><a class="dropdown-item" href="#">Something else here</a></li>
    </ul>
  </div>
</div> -->

    <div>
        <select v-model="selectedFile" class="form-select form-select-lg mb-3" aria-label=".form-select-lg example">
          <option value="1">Apiori</option>
          <option value="2">CF</option>
        </select>
      <div v-if="selectedFile === '1'">
        <div class="row">
          <div class="col">
            <label for="Support" class="form-label">Support</label>
        <input  type="range" class="form-control-range" id="Support" v-model="Support">
        <span ><h3>{{Support}} %</h3></span>
          </div>
          <div class="col">
            <label for="Confidence" class="form-label">Confidence</label>
            <input  type="range" class="form-control-range" id="Confidence" v-model="Confidence">
            <span ><h3>{{Confidence}} %</h3></span>
          </div>
        <div class="row">
          <div class="col">
            <h6>Sort By</h6>
            <div class="form-check">
              <input type="radio" class="form-check-input" id="radio1" name="optradio" value="option1" checked>Confidence
              <label class="form-check-label" for="radio1"></label>
            </div>
            <div class="form-check">
              <input type="radio" class="form-check-input" id="radio2" name="optradio" value="option2">Lift
              <label class="form-check-label" for="radio2"></label>
            </div>
          </div>
        </div>
          </div>
        <button @click="submit" class="btn btn-primary">Submit</button>
    </div>
    <div  v-if="selectedFile === '2'">
        <div class="row">
          <div class="col">
            <label for="Support" class="form-label">Latent Factor</label>
        <input  type="range" class="form-control-range" id="Support" max = 33 v-model="latent">
        <span ><h3>K {{latent}}</h3></span>
          </div>
          </div>
        <button  @click="submit2" class="btn btn-primary">Submit</button>
    </div>
  </div>



  <!-- Position it: -->
  <!-- - `.toast-container` for spacing between toasts -->
  <!-- - `top-0` & `end-0` to position the toasts in the upper right corner -->
  <!-- - `.p-3` to prevent the toasts from sticking to the edge of the container  -->


</div>

</template>
<script>

// $(document).ready(function () {
//   $(".toast").toast('show');
// });
import table from "../components/table2.vue"
import axios from '../axios.js';
export default {
  data() {
    return {
      Support: 50,
      Confidence: 50,
      latent: 15,
      files: [],
      selectedFile: "",
      check: ''
    }
  },
  methods: {
    submit1() {
      // Perform some action with the selected file
      console.log(this.selectedFile)
      console.log(this.value)
      $(".toast").toast('show');
    },
    submit2() {
      console.log(this.latent)
      axios.post('/save', {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        values: this.latent
      })
        .then(response => {
          this.check = response.data['msg']
        })
      $(".toast").toast('show');
    }
  },

}
</script>
<style lang="">
    
</style>