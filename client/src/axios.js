import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    "Content-Type": "application/json",
    "apikey": "dQPsrJnjyrkPHFHbCiqdrxki6ulZ8qDS",
},
});

instance.interceptors.request.use(function (config) {
    config.headers.Authorization = 'Bearer ' + localStorage.getItem('token');
    return config;
});

export default instance;

