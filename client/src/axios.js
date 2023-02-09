import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://127.0.0.1:5001',
  
});

instance.interceptors.request.use(function (config) {
    config.headers.Authorization = 'Bearer ' + localStorage.getItem('token');
    return config;
});

export default instance;

