<template lang="">
  <q-layout view="hHh lpR fFf ">
    <q-page-container>

      <q-page class="flex flex-center ">
        
        <q-card class="text-left  ">
          <q-card-section >
            <h1 class="Login">Login system</h1>
            <q-form @submit.prevent="login" class="q-gutter-y-md" >
            <q-input v-model="email" type="username" label="Username" class="mb-4" :rules="[ val => val && val.length > 0 || 'Please type something']"/>
            <q-input v-model="password" type="password" label="Password" class="mb-4" :rules="[ val => val && val.length > 0 || 'Please type something']" />
            <q-btn @click="login" type="submit" color="dark" label="Sign in"  class="mt"/>
            </q-form>
          </q-card-section>
        </q-card>
      
      </q-page>

    </q-page-container>
  </q-layout>
</template>
<script>
import axios from '../axios.js'
// import { mapActions } from 'vuex'
// import store from '../store'
import { useQuasar, QSpinnerFacebook } from 'quasar'

export default {
  data() {
    return {
      email: '',
      password: '',
    }
  },
  methods: {
    login() {
      this.$q.loading.show({
        spinner: QSpinnerFacebook,

        spinnerSize: 140,

        message: 'Please wait',
        messageColor: 'white'
      })

      axios.post('/login', {
        username: this.email,
        password: this.password
      })
        .then(response => {
          localStorage.setItem('token', response.data.access_token);
          console.log(localStorage.getItem('token'))
          this.$store.dispatch('getCurrentUser')

          setTimeout(() => {
            this.$q.loading.hide()
            this.$router.push("/home");
          }, 2000)
        })
        .catch(error => {
          if (error.response.status === 401) {
            setTimeout(() => {
              this.$q.loading.hide();
              this.$q.notify({
                color: "negative",
                position: "top",
                message: "Your password or username may be wrong, try again."
              });
            }, 2000)
          }
        });
    }
  }
}

</script>
<style>


.rounded {
    
    border-radius: 10px 10px 10px 10px;
}


</style>