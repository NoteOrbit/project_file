import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store.js'
import "./plugin/chart.js"
import './scss/styles.scss'
import * as bootstrap from 'bootstrap'

const app = createApp(App);

app.use(router);
app.use(store);

app.mount('#app') 
