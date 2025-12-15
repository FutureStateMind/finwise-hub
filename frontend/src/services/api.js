import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  }
});

// CSRF token handling
api.interceptors.request.use((config) => {
  const csrfToken = getCookie('csrftoken');
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register/', data),
  login: (credentials) => api.post('/auth/login/', credentials),
  logout: () => api.post('/auth/logout/'),
  getCurrentUser: () => api.get('/auth/me/'),
  getProfile: () => api.get('/auth/profile/'),
  updateProfile: (data) => api.patch('/auth/profile/', data),
};

// Finance API
export const financeAPI = {
  // Bank Accounts
  getBankAccounts: () => api.get('/finance/bank-accounts/'),
  getBankAccount: (id) => api.get(`/finance/bank-accounts/${id}/`),
  createBankAccount: (data) => api.post('/finance/bank-accounts/', data),
  updateBankAccount: (id, data) => api.put(`/finance/bank-accounts/${id}/`, data),
  deleteBankAccount: (id) => api.delete(`/finance/bank-accounts/${id}/`),
  
  // Renewals
  getRenewals: () => api.get('/finance/renewals/'),
  getRenewal: (id) => api.get(`/finance/renewals/${id}/`),
  createRenewal: (data) => api.post('/finance/renewals/', data),
  updateRenewal: (id, data) => api.put(`/finance/renewals/${id}/`, data),
  deleteRenewal: (id) => api.delete(`/finance/renewals/${id}/`),
  
  // Investments
  getInvestments: () => api.get('/finance/investments/'),
  getInvestment: (id) => api.get(`/finance/investments/${id}/`),
  createInvestment: (data) => api.post('/finance/investments/', data),
  updateInvestment: (id, data) => api.put(`/finance/investments/${id}/`, data),
  deleteInvestment: (id) => api.delete(`/finance/investments/${id}/`),
};

// AI Advisor API
export const aiAPI = {
  getFullAnalysis: () => api.get('/ai/analysis/'),
  getInvestmentAnalysis: () => api.get('/ai/analysis/investments/'),
  getCashFlowAnalysis: () => api.get('/ai/analysis/cash-flow/'),
  getRecommendations: () => api.get('/ai/recommendations/'),
};

export default api;
