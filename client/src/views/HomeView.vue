<script setup>
import box from '../components/box.vue'
import table2 from '../components/table2.vue'
import chart from '../components/bar.vue'
</script>


<template>
  <!-- <navbar /> -->
  <div class="container ">
    <div class="jumbotron my-3">
      <h1 class="display-4">Welcome {{ currentUser }} 👨🏻‍💻</h1>
    </div>
    <box/>
    <h1>
        Traffic
    </h1>
    <chart/>
    <!-- <div class="container">
        <div class="row d-flex justify-content-center align-items-center h-100">
            <div class="col-lg-12 col-xl-11">
                <div class="card text-black" style="border-radius: 25px;">
                    <div class="card-body p-md-5">
                        <div class="row justify-content-center">
                            <div class="col-md-10 col-lg-6 col-xl-5 order-2 order-lg-1">

                                <p class="text-center h1 fw-bold mb-5 mx-1 mx-md-4 mt-4">TEST COLLECTIONS DATA</p>
                                <form @submit.prevent="register">
                                    <div class="form-group">
                                        <label for="username">Username</label>
                                        <input type="text" id="username" v-model="username" class="form-control" />
                                    </div>
                                    <div class="form-group">
                                        <label for="name">Name</label>
                                        <input type="text" id="name" v-model="name" class="form-control" />
                                    </div>
                                    <div class="form-group">
                                        <label for="email">Email</label>
                                        <input type="email" id="email" v-model="email" class="form-control" />
                                    </div>
                                    <div class="form-group">
                                        <label for="password">Password</label>
                                        <input type="password" id="password" v-model="password" class="form-control" />
                                    </div>
                                
                                    <button class="btn btn-primary" type="submit">POST</button>
                                </form>

                            </div>
                            <div class="col-md-10 col-lg-6 col-xl-7 d-flex align-items-right">

                                <img src="https://i.pinimg.com/originals/d7/c2/50/d7c250296c3c3b44c9aeb01623dd1023.gif"
                                    class="img-fluid" alt="Sample image">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
     -->

</div>
  <!-- </style> -->

</template>
<script>
import axios from '../axios.js';
import '@/assets/style.css'
import { mapGetters } from 'vuex'
export default {
  computed: {
    ...mapGetters(['currentUser'])
  },
  name: "Home",
  data() {
    return {

    }
  },

}
</script>
<style>

</style>
