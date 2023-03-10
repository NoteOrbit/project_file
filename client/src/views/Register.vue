<template lang="">
    <q-layout view="hHh lpR fFf ">
      <q-page-container>
  
        <q-page class="flex flex-center ">
        
          <q-card class="text-left  q-ma-md">
            <q-card-section >
              <h2 class="Login"><q-icon name="login" /> Register Dashboard</h2>
              <q-form @submit.prevent="register" class="q-gutter-y-md" >
                <q-input v-model="name" type="name" label="Name" class="mb-4" :rules="[ val => val && val.length > 0 || 'Please type something']"/> 
                <q-input v-model="username" type="username" label="Username" class="mb-4" :rules="[ val => val && val.length > 0 || 'Please type something']"/>
              <q-input v-model="password" type="password" label="Password" class="mb-4" :rules="[ val => val && val.length > 0 || 'Please type something']" />
              <q-input v-model="email" type="email" label="Email" class="mb-4" :rules="[ val => val && val.length > 0 || 'Please type something']"/>   
              <q-btn @click="register" type="submit" color="dark" label="Register"  class="mt"/>
              </q-form>
            </q-card-section>
          </q-card>
        
        </q-page>
  
      </q-page-container>
    </q-layout>
  </template>

<script>
import axios from '../axios.js'

export default {
    data() {
        return {
            username: '',
            name:'',
            email: '',
            password: '',
            response: ''
        }
    },
    methods: {
        register() {
            axios.post('/Register', {
                username: this.username,
                name:this.name,
                email: this.email,
                password: this.password
            })
                .then(response => {
                    this.response = response.status
                    if(response.status === 201){
                        this.$router.push({name:'login'})
                    }
                    // Do something with the response, like redirecting to the login page
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>