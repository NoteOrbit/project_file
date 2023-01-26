import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store.js'
import '../src/scss/styles.scss'
import * as bootstrap from 'bootstrap'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import "./plugin/chart.js"
const app = createApp(App);


app.use(router);
app.use(store);

app.mount('#app') 
