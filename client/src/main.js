import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store.js'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import "./plugin/chart.js"
import './scss/styles.scss'
import "bootstrap/dist/js/bootstrap.js";
// Import all of Bootstrap's JS
import * as bootstrap from 'bootstrap'


const app = createApp(App);


app.use(router);
app.use(store);

app.mount('#app') 
