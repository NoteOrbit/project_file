import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://192.168.1.52:5000',
  
});

instance.interceptors.request.use(function (config) {
    config.headers.Authorization = 'Bearer ' + localStorage.getItem('token');
    return config;
});

export default instance;