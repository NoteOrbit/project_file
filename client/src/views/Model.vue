
<template>
  <q-layout>

    <q-page-container>
      <q-page>
        <div class="q-pa-md">
          <div class="col">
            <div class="flex justify-center">
              <span>
                <h4>Management Model Control</h4>
              </span>
            </div>
            <q-intersection
        :key="index"
        transition="jump-up"
      >
            <div class="row justify-center q-gutter-sm ">
              
              <div class="col-12 col-md-auto">
                <q-card class="my-card bg-black text-white w">

                  <q-card-section>
                    <h5> <q-icon name="handshake"/> Collaborative filtering</h5>
                    <strong>versions {{ current }}</strong>
                  </q-card-section>

                </q-card>
              </div>
              <div class="col-12 col-md-auto">


                <q-card class="my-card bg-red-10 text-white">

                  <q-card-section>
                    <h5><q-icon name="rule"/> Associations rules</h5>
                    <strong>versions {{ current_as }}</strong>
                  </q-card-section>

                </q-card>
              </div>
            </div>
            </q-intersection>


            <div>

              <calendar />
              <div class="flex flex-center">
                <q-toggle checked-icon="check" size="L" v-model="checked" color="green"
                  :label="`System that will allow you to retrain the model every 6 hours.`"
                  @update:model-value="checkAPIStatus" />
              </div>
            </div>

          </div>
        </div>

        <div v-if="checked != true">
          <div class="q-pa-md flex flex-center">
            <p></p>
            <q-btn-dropdown color="black" dropdown-icon="change_history" label="Model">

              <q-list>
                <q-item v-for="option in selectOptions" :key="option.value" clickable v-close-popup
                  @click="selectedFile = option.value">

                  <q-item-section>{{ option.label }}</q-item-section>
                </q-item>
              </q-list>
            </q-btn-dropdown>
          </div>
        </div>



        <div v-if="selectedFile === '1' && checked != true">
          <q-intersection
        :key="index"
        transition="jump-up"
      >
          <q-card class="q-pa-md" style="margin: 0 auto; width: 90%;">
            <q-card-section>
              <q-slider v-model="Support" label-always :min="1" :max="15" />
              <span>Support</span>
              <q-slider v-model="Confidence" label-always :min="0" :max="100" />
              <span>Threshold</span>
            </q-card-section>
            <q-card-section>
              <q-item-label header>Sort By</q-item-label>
              <q-item>
                <q-radio v-model="sortBy" val="confidence" label="Confidence" required />
              </q-item>
              <q-item>
                <q-radio v-model="sortBy" val="lift" label="Lift" required />
              </q-item>
            </q-card-section>
            <q-card-section>
              <q-item-label header>Base On</q-item-label>
              <q-item>
                <q-radio v-model="BaseOn" val="like" label="Like" required />
              </q-item>
              <q-item>
                <q-radio v-model="BaseOn" val="view" label="View" required />
              </q-item>
            </q-card-section>
            <q-card-actions align="right">
              <q-btn color="primary" @click="submit1">Submit</q-btn>
              <q-btn color="secondary" @click="reset">Cancel</q-btn>
            </q-card-actions>
          </q-card>

        </q-intersection>
        </div>

        <div v-if="selectedFile === '2' && checked != true">
          <q-intersection
        :key="index"
        transition="jump-up"
      >
          <q-card class="q-pa-md " style="margin: 0 auto; width: 90%;">
            <q-card-section>

              <q-slider v-model="latent" label="Latent Factor" label-always :min="0" :max="33" />
              <span>K values</span>
            </q-card-section>
            <q-card-actions align="right">
              <q-btn color="primary" @click="submit2">Submit</q-btn>
              <q-btn color="secondary" @click="reset">Cancel</q-btn>
            </q-card-actions>
          </q-card>
        </q-intersection>
        </div>


      <!-- <h4 class="my-3">Manual retraining</h4>
        <select v-model="selectedFile" class="form-select form-select-lg mb-3" aria-label=".form-select-lg example">
          <option value="1">Apriori</option>
          <option value="2">CF</option>
              </select> -->


      <!-- <div v-if="selectedFile === '1'">
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
           -->




      <!-- 
        </div> -->
      <!-- <div class="q-gutter-y-md column" style="max-width: 300px">
    <q-select filled v-model="model" :options="options" label="Filled" />
        </div> -->








        <div>
          <div class="q-pa-md">
            <div class="col">
              <span>
                <h4>Selected Model Version</h4>
              </span>
            </div>
          </div>

          <div class="a">
            <q-table title="Log" :rows='models' :columns="tableColumns" :pagination="{
              type: 'normal',
              rowsPerPage: 5,
              rowsPerPageOptions: [10, 20, 50],
              prevIcon: 'mdi-chevron-left',
              nextIcon: 'mdi-chevron-right',
              noDataIcon: 'mdi-emoticon-sad'
            }" :filter="filter1" row-key="_id">
              <template v-slot:top-right>
                <q-input borderless dense debounce="300" v-model="filter1" placeholder="Search">
                  <template v-slot:append>
                    <q-icon name="search" />
                  </template>
                </q-input>
              </template>

              <template v-slot:body="{ row }">

                <q-tr>
                  <q-td>{{ row._id }}</q-td>
                  <q-td>{{ row.model_name }}</q-td>
                  <q-td>{{ row.date }}</q-td>
                  <q-td>{{ row.path }}</q-td>
                  <q-td>{{ row.measures ? row.measures.mse : '-' }}</q-td>
                  <q-td>{{ row.setting ? row.setting : '-' }}</q-td>
                  <q-td>
                    <!-- <q-btn color="primary" @click="switchModel(row)">Use This Model</q-btn> -->
                    <q-btn color="black" @click="row.model_name === 'CF' ? switchModel(row) : switchModel_AS(row)">
                      Use model
                    </q-btn>
                  </q-td>
                </q-tr>
              </template>
            </q-table>

          </div>
        </div>




      </q-page>
    </q-page-container>





  </q-layout>

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
</template>
<script>

// $(document).ready(function () {
//   $(".toast").toast('show');
// });

import { useQuasar, QSpinnerFacebook } from 'quasar';
import axios from '../axios.js';
import { ref } from 'vue'
import calendar from '../components/calendar.vue';
export default {
  components: {
    calendar
  },
  setup() {
    return {
      filter1: ref(''),

    }
  },
  data() {
    return {
      selectOptions: [
        {
          label: 'Associations rules',
          value: '1'
        },
        {
          label: 'Collaborative filtering',
          value: '2'
        }
      ],
      selectedbaseon: ref(null),
      BaseOn: '',
      statusMessage: '',
      models: [],
      Support: 5,
      Confidence: 50,
      sortBy: "",
      current: "",
      current_as: "",
      latent: 15,
      files: [],
      selectedFile: ref(""),
      check: '',
      Status: ref(null),
      checked: ref(true),
      running: false,
      paused: false,
      pageSize: 5,
      currentPage: 1,

      tableColumns: [
        { name: '_id', label: 'ID', field: '_id', align: 'left' },
        { name: 'model_name', label: 'MODEL', field: 'model_name', align: 'left', sortable: true },
        { name: 'date', label: 'DATE', field: 'date', align: 'left', sortable: true },
        { name: 'path', label: 'PATH', field: 'path', align: 'left' },
        { name: 'mse', label: 'MSE', field: 'measures', align: 'left' },
        { name: 'setting', label: 'SETTING', field: 'setting', align: 'left' },
        { name: 'actions', label: 'ACTIONS', align: 'left', },
        // { name: 'setting', label: 'SETTING', field: row => this.models.setting.k, align: 'left' },
      ],
    }
  },
  created() {
    this.fetchModels();
  },
  methods: {
    reset() {
      this.selectedFile = ''
    },
    update_values(value) {
      this.selectedFile = value
    },
    submit1() {
      this.$q.loading.show({
        spinner: QSpinnerFacebook,

        spinnerSize: 140,

        message: 'Please wait',
        messageColor: 'white'
      })
      console.log(this.Support)
      console.log(this.Confidence)
      console.log(this.sortBy)
      console.log(this.BaseOn)
      axios.post('save_as', {
        headers: {
          'Content-Type': 'application/json',
        },
        sup: this.Support,
        con: this.Confidence,
        metric: this.sortBy,
        base_on: this.BaseOn
      })
        .then(response => {
          this.check = response.data['msg']
          if (response.status === 201) {
            this.$q.loading.hide()
            this.$q.notify({
              color: "positive",
              message: "Training Success",
              position: "top-right"
            })
          }
        }).catch(error => {
          this.$q.loading.hide()
          this.$q.notify({
            color: "negative",
            message: "Training Failed",
            position: "top-right"
          })
          console.log(error)
        })
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
      location.reload();
    },
    async fetchModels() {
      try {
        const res = await axios.get("/getmodel");

        this.models = res.data;
        console.log(this.models)
      } catch (error) {
        console.log(error);
      }
    },
    async switchModel(model) {
      try {
        const response = await axios.post("/switch_model", { path: model.path });

        if (response.status === 200) {
          this.$q.notify({
            color: "positive",
            message: "Model switched successfully",
            position: "top-right"
          });
          location.reload();
        }
      } catch (error) {
        console.log(error);
        this.$q.notify({
          color: "negative",
          message: "An error occurred while switching the model",
          position: "top-right"
        });
      }
    },
    async switchModel_AS(model) {
      try {
        const response = await axios.post("/switch_model_as", { path: model.path });

        if (response.status === 200) {
          this.$q.notify({
            color: "positive",
            message: "Model switched successfully",
            position: "top-right"
          });
          location.reload();
        }
      } catch (error) {
        console.log(error);
        this.$q.notify({
          color: "negative",
          message: "An error occurred while switching the model",
          position: "top-right"
        });
      }
    },
    async checkAPIStatus() {
      try {
        let response
        if (this.checked) {
          response = await axios.get('resume_job')
          this.paused = true
          this.running = false
          this.$q.notify({
            color: "positive",
            message: "Running interval",
            position: "top-right"
          });
        } else {
          response = await axios.get('pause_job')
          this.paused = false
          this.running = true
          this.$q.notify({
            color: "negative",
            message: "Pause interval",
            position: "top-right"
          });
        }
        if (response.status === 200) {
          this.Status = response.data
          console.log(this.Status.msg)
          this.statusMessage = this.Status.msg


        }
      } catch (error) {
        console.log(error)
        this.checked = !this.checked
      }
    },
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
    try {
      const response1 = await axios.get('get_current')
      if (response1.status === 200) {
        console.log(response1)
        this.current = response1.data['model_cf']
        this.current_as = response1.data['model_as']
      }
    } catch (error) {
    }
  },


}
</script>
<style lang="sass">

.a
  padding: 10px

</style>