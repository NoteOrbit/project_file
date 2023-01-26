<template lang="">
<div>
  <div class="toast-container top-0 end-0 p-3">

<!-- Then put toasts within -->
<div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
  <div class="toast-header">
    <img src="https://thumbs.gfycat.com/GrouchyElegantAlbacoretuna-max-1mb.gif" width="100" height="100" class="rounded me-2" alt="...">
    <strong class="me-auto">Bootstrap</strong>
    <small class="text-muted">just now</small>
    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
  </div>
  <div class="toast-body">
    you want to change model ?
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
  <h1 class="my-3">Settings</h1>
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

<bar/>
<div>
    <select v-model="selectedFile" class="form-select form-select-lg mb-3" aria-label=".form-select-lg example">
      <option v-for="file in files" :value="file">{{ file }}</option>
    </select>
  </div>
  <div aria-live="polite" aria-atomic="true" class="position-relative">
  <!-- Position it: -->
  <!-- - `.toast-container` for spacing between toasts -->
  <!-- - `top-0` & `end-0` to position the toasts in the upper right corner -->
  <!-- - `.p-3` to prevent the toasts from sticking to the edge of the container  -->



</div>
</div>
</template>
<script>
  $(document).ready(function() {
      $(".toast").toast('show');
  });
import axios from '../axios.js';
export default {
  data() {
    return {
      files: [],
      selectedFile: ""
    }
  },
  created() {
    axios.get('/model').then(response => {
      this.files = response.data;
    });
  }
}
</script>
<style lang="">
    
</style>