import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:5000',
  
});

instance.interceptors.request.use(function (config) {
    config.headers.Authorization = 'Bearer ' + localStorage.getItem('token');
    return config;
});

export default instance;