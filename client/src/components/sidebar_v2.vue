<template>
  <q-header elevated class="bg-black">
    <q-toolbar>
      <q-toolbar-title>Recommendation system beackend</q-toolbar-title>
      <q-btn flat @click="drawer = !drawer" round dense icon="menu" />
    </q-toolbar>
  </q-header>

  <q-drawer v-model="drawer" show-if-above :width="200" :breakpoint="400">
    <q-scroll-area style="height: calc(100% - 150px); margin-top: 150px; border-right: 1px solid #ddd">

      <q-list padding>
        <q-item clickable v-ripple @click="$router.push('/home')">
          <q-item-section avatar>
            <q-icon name="home" />
          </q-item-section>
          <q-item-section>
            Home
          </q-item-section>
        </q-item>
        <q-item clickable v-ripple @click="$router.push('/Model')">
          <q-item-section avatar>
            <q-icon name="model_training" />
          </q-item-section>
          <q-item-section>
            Management model
          </q-item-section>
        </q-item>
        <q-item clickable v-ripple @click="$router.push('/Transaction')">
          <q-item-section avatar>
            <q-icon name="route" />
          </q-item-section>
          <q-item-section>
            Transaction
          </q-item-section>
        </q-item>
        <q-item clickable v-ripple @click='logoutDialog = true'>
          <q-item-section avatar>
            <q-icon name="exit_to_app"/>
          </q-item-section>
          <q-item-section>
            Logout
          </q-item-section>
        </q-item>
      </q-list>
      <q-dialog v-model="logoutDialog" persistent>
          <q-card>
            <q-card-section class="row items-center">
              <q-avatar icon="exit_to_app" color="black" text-color="white" />
              
              <span class="q-ml-sm">Are you sure you want to logout?</span>
            </q-card-section>
        
    


            <q-card-actions align="right">
              <q-btn flat label="Cancel" color="primary" @click="logoutDialog = false" />
              <q-btn flat label="Logout" color="negative" @click="logout" />
            </q-card-actions>
          </q-card>
        </q-dialog>
    </q-scroll-area>

    <q-img class="absolute-top" src="https://images.unsplash.com/photo-1616712134411-6b6ae89bc3ba?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8NXx8fGVufDB8fHx8&w=1000&q=80" style="height: 150px">
      <div class="absolute-bottom bg-transparent">
        <q-avatar size="56px" class="q-mb-sm">
          <img src="../assets/proflie.png">
        </q-avatar>
        <div class="text-weight-bold">{{ currentUser }}</div>
        <div>@Data Sci</div>
      </div>
    </q-img>
  </q-drawer>
</template>

<script>
import { ref } from 'vue'
export default {
  setup() {
    return {
      drawer: ref(false),
      logoutDialog: ref(false),
      cancelEnabled: ref(false)
      
    }
  },
  currentDateTime: '',
  computed: {
    currentUser() {
      return this.$store.state.currentUser;
    }
  },

  
  created() {
    console.log(this.currentUser);
    this.updateDateTime()
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push({ name: 'login' });
    },
    updateDateTime() {
      this.currentDateTime = new Date().toLocaleString()
      setTimeout(this.updateDateTime, 1000)
    }
  }
}

</script>