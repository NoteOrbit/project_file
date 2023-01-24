<template lang="">
  <div class="container">
    <section class="vh-100">
  <div class="container py-5 h-100">
    <div class="row d-flex align-items-center justify-content-center h-100">
      <div class="col-md-8 col-lg-7 col-xl-6">
        <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.svg"
          class="img-fluid" alt="Phone image">
      </div>
      <div class="col-md-7 col-lg-5 col-xl-5 offset-xl-1">
        <h1 class="Login">Login system</h1>
        <form @submit.prevent="login">
          <!-- Email input -->
          <div class="form-outline mb-4">
            <input type="username" id="form1Example13" v-model ='email' class="form-control form-control-lg" />
            <label class="form-label" for="form1Example13">Username</label>
          </div>

          <!-- Password input -->
          <div class="form-outline mb-4">
            <input type="password" id="form1Example23" v-model ='password' class="form-control form-control-lg" />
            <label class="form-label" for="form1Example23">Password</label>
          </div>

          <!-- Submit button -->
          <router-link to="/home">
            <button @click="login" class="btn btn-primary btn-lg btn-block">Sign in</button>
          </router-link>
          <router-link to="/Register">
            <button class="btn btn-dark btn-lg btn-block">Register</button>
          </router-link>
        </form>
      </div>
    </div>
  </div>
</section>
  </div>
</template>
<script>
import axios from '../axios.js'
import { mapActions } from 'vuex'
import store from '../store'
export default {
  data() {
    return {
      email: '',
      password: '',
    }
  },
  methods: {
    login() {
      axios.post('/login', {
        username: this.email,
        password: this.password
      })
        .then(response => {
          localStorage.setItem('token', response.data.access_token);
          console.log(localStorage.getItem('token'))
          this.$store.dispatch('getCurrentUser')
          // Do something with the token, like redirecting to a protected route
        })
        .catch(error => {
          console.log(error);
        });
    }
  }
}
</script>
<style>
  .Login {
    
    margin-top: 25px;
    margin-bottom: 25px;
  }
  .btn {
    margin-top: 10px;
  }
</style>