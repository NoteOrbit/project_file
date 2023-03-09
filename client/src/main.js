
import App from './App.vue'
import router from './router'
import store from './store.js'
import "./plugin/chart.js"
// import './scss/styles.scss'

// import * as bootstrap from 'bootstrap'
// import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'
import { createApp } from 'vue'
import { Quasar,Notify,Loading} from 'quasar'

import Plugin from '@quasar/quasar-ui-qcalendar/src/QCalendarDay.js'
import '@quasar/quasar-ui-qcalendar/src/css/calendar-day.sass'
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'
import Particles from "vue3-particles";


const app = createApp(App);

app.use(Quasar, {
    plugins: {
        Notify,
        Loading
    },
    config:{
        Notify:{},
        loading:{}
    },

  })


app.use(router);
app.use(store);
app.use(Plugin);
app.use(Particles)
app.mount('#app') 

