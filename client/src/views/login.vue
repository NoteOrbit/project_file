<template lang="">
  <q-layout view="hHh lpR fFf ">
    <q-page-container>

      <q-page class="flex flex-center ">
        <q-intersection
        :key="index"
        transition="jump-down"
      >
        <q-card class="text-left  q-ma-md">
          <q-card-section >
            <h2 class="Login"><q-icon name="login" /> Login Dashboard</h2>
            <q-form @submit.prevent="doLogin" class="q-gutter-y-md" >
            <q-input v-model="email" type="username" label="Username" class="mb-4" :rules="[ val => val && val.length > 0 || 'Please type something']"/>
            <q-input v-model="password" type="password" label="Password" class="mb-4" :rules="[ val => val && val.length > 0 || 'Please type something']" />
            <q-btn @click="doLogin" type="submit" color="dark" label="Sign in"  class="mt"/>
            </q-form>
          </q-card-section>
        </q-card>
      </q-intersection>
      </q-page>

    </q-page-container>
  </q-layout>
</template>
<script>
import { useQuasar, QSpinnerFacebook } from 'quasar'
import { mapActions } from 'vuex';
export default {
  data() {
    return {
      email: '',
      password: '',
    }
  },
  methods: {
    ...mapActions(['login']),
    
    async doLogin() {

      const success = await this.login({
        username: this.email,
        password: this.password,
      });
      if (success) {
        this.$router.push('/home');
      }
       else {
        this.$q.notify({
          color: "negative",
                position: "top",
                message: "Your password or username may be wrong, try again."
        });
      }
    },
  },
};


</script>
<style>


.rounded {
    
    border-radius: 10px 10px 10px 10px;
}


</style>