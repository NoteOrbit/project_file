
import App from './App.vue'
import router from './router'
import store from './store.js'
import "./plugin/chart.js"
// import './scss/styles.scss'

// import * as bootstrap from 'bootstrap'
// import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'
import { createApp } from 'vue'
import { Quasar,Notify,Loading } from 'quasar'

// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'

// Import Quasar css
import 'quasar/src/css/index.sass'




const app = createApp(App);

app.use(Quasar, {
    plugins: {
        Notify,
        Loading
    },
    config:{
        Notify:{},
        loading:{}
    } 
  })


app.use(router);
app.use(store);

app.mount('#app') 
