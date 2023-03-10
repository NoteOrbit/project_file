import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://0.0.0.0:8000',
  headers: {
    "Content-Type": "application/json",
    "apikey": "Lp0sJNLUiREPno2Rtv2GMFNukpdtDxsC",
},
});

instance.interceptors.request.use(function (config) {
    config.headers.Authorization = 'Bearer ' + localStorage.getItem('token');
    return config;
});

export default instance;

