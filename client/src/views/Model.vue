<template lang="">
<div>
  <div>
    <toast-component ref="toast" :msg="Status" @show-toast="showToast"></toast-component>
  </div>
</div>
<div class="container-lg my-2">
  <!-- <div class="row">
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
  <hr class="mt-10 mb-1"/> -->
  
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

  <div class="my-4">
  <div class="row">
    <span><h4>Automatic retraining</h4></span>
    <span><p>System that will allow you to retrain the model every 6 hours.</p></span>
    <span><h6>Status {{ Status }}</h6></span>
    <div class="col">
      <div class="form-check form-switch">
        <input class="form-check-input " type="checkbox" role="switch" v-model="checked" @change="checkAPIStatus()" id="flexSwitchCheckDefault" >
        <label class="form-check-label" for="flexSwitchCheckDefault">Status</label>
      </div>
    </div>
  </div>
</div>

<div v-if="checked != true">
  <h4 class="my-3">Manual retraining</h4>
        <select v-model="selectedFile" class="form-select form-select-lg mb-3" aria-label=".form-select-lg example">
          <option value="1">Apriori</option>
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
  <hr class="mt-10 mb-1"/>
  <div class="my-4">
  <div class="row">
    <span><h4>Selected Model Verersion</h4></span>
    <span><p>System that will use model.</p></span>
<div class="row">
  <div class="col">
  <span>Apriori</span>
  <select class="form-select form-select-lg mb-3" aria-label=".form-select-lg example">
  <option selected>Open this select menu</option>
  <option value="1">One</option>
  <option value="2">Two</option>
  <option value="3">Three</option>
</select>

  </div>
  <div class="col">
  <span>CF</span>
  <select class="form-select form-select-lg mb-3" aria-label=".form-select-lg example">
  <option selected>Open this select menu</option>
  <option value="1">One</option>
  <option value="2">Two</option>
  <option value="3">Three</option>
</select>
  </div>
</div>
  </div>
</div>
  <!-- Position it: -->
  <!-- - `.toast-container` for spacing between toasts -->
  <!-- - `top-0` & `end-0` to position the toasts in the upper right corner -->
  <!-- - `.p-3` to prevent the toasts from sticking to the edge of the container  -->
  <!-- <div>
    <h1>Model Switch</h1>
    <table class="table">
      <thead>
        <tr>
          <th>Path</th>
          <th>Date</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="model in models" :key="model._id" :class="{ 'table-active': model === selectedModel }">
          <td>{{ model.path }}</td>
          <td>{{ model.date }}</td>
          <td>
            <button class="btn btn-primary" @click="switchModel(model)">Use This Model</button>
            <button class="btn btn-danger" @click="deleteModel(model)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div> -->


  
  <div>
    <h1>Model Switch</h1>
    <table class="table">
      <thead>
        <tr>
          <th>Path</th>
          <th>Date</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="model in currentModels" :key="model._id" :class="{ 'table-active': model === selectedFile }">
          <td>{{ model.path }}</td>
          <td>{{ model.date }}</td>
          <td>
            <button class="btn btn-primary mr-2" @click="switchModel(model)">Use This Model</button>
            <!-- <button class="btn btn-danger" @click="deleteModel(model)">Delete</button> -->
          </td>
        </tr>
      </tbody>
    </table>
    <nav aria-label="Page navigation">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <a class="page-link" href="#" @click.prevent="goToPage(currentPage - 1)">Previous</a>
        </li>
        <li class="page-item" v-for="page in pages" :key="page" :class="{ active: currentPage === page }">
          <a class="page-link" href="#" @click.prevent="goToPage(page)">{{ page }}</a>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <a class="page-link" href="#" @click.prevent="goToPage(currentPage + 1)">Next</a>
        </li>
      </ul>
    </nav>
  </div>


</div>

</template>
<script>

// $(document).ready(function () {
//   $(".toast").toast('show');
// });
import table from "../components/table2.vue"
import axios from '../axios.js';
import ToastComponent from '../components/noti.vue'

export default {
  components: {
    ToastComponent
  },
  data() {
    return {
      statusMessage: '',
      loaded: false,
      models: [],
      Support: 50,
      Confidence: 50,
      latent: 15,
      files: [],
      selectedFile: "",
      check: '',
      Status: "",
      checked: true,
      running: false,
      paused: false,
      pageSize: 5,
      currentPage: 1,
    }
  },
  created() {
    this.fetchModels();
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
      axios.post('save_cf', {
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
    },
    async fetchModels() {
      this.loaded = false
      try {
        const res = await axios.get("/getmodel");
        this.models = res.data;
      } catch (error) {
        console.log(error);
      }
    },
    async switchModel(model) {
      try {
        await axios.post("/switch_model", { path: model.path });
      } catch (error) {
        console.log(error);
      }
    },
    async checkAPIStatus() {
      console.log(this.Status)
      try {
        let response
        if (this.checked) {
          response = await axios.get('resume_job')
          this.paused = true
          this.running = false
        } else {
          response = await axios.get('pause_job')
          this.paused = false
          this.running = true
        }
        if (response.status === 200) {
          this.Status = response.data
          console.log(this.Status.msg)
          this.statusMessage = this.Status.msg
          this.showToast()

          
        }
      } catch (error) {
        console.log(error)
        this.checked = !this.checked
      }
    },
    showToast() {
      this.$refs.toast.showToast = true
    },

    goToPage(page) {
      
      this.currentPage = page;
  }
  },
  async mounted() {
    try {
      const response = await axios.get('check_job')
      if (response.status === 200) {
        this.checked = true
        this.Status = response.data
      } else {
        this.checked = false
        this.Status = response.data
      }
    } catch (error) {
      this.checked = false
    }

  },
  computed: {
    totalPages() {
      
      return Math.ceil(this.models.length / this.pageSize)
    },
    pages() {
      console.log(this.totalPages)
      return Array.from({ length: this.totalPages }, (_, i) => i + 1)
    },
    currentModels() {
      
      const startIndex = (this.currentPage - 1) * this.pageSize
      console.log(startIndex)
      return this.models.slice(startIndex, startIndex + this.pageSize)
    }
  },

}
</script>
<style lang="">


</style>