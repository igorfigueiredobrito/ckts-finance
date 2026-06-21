import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5001/api', // Flask API URL
  timeout: 10000,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Se o backend retornar 401, remove o token e redireciona pro Login
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      
      // Só redireciona se a rota atual não for de login e a requisição não for para /login
      if (!window.location.pathname.includes('/login') && !error.config.url.includes('/login')) {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;
