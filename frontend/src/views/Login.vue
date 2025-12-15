<template>
  <div class="login-container">
    <div class="login-card">
      <h1>FinWise Hub</h1>
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input 
            type="text" 
            id="username" 
            v-model="credentials.username" 
            required
            placeholder="Enter your username"
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="credentials.password" 
            required
            placeholder="Enter your password"
          />
        </div>
        <div v-if="error" class="error-message">{{ error }}</div>
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      <p class="register-link">
        Don't have an account? <router-link to="/register">Register here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authAPI } from '../services/api';

export default {
  name: 'Login',
  setup() {
    const router = useRouter();
    const credentials = ref({
      username: '',
      password: ''
    });
    const error = ref('');
    const loading = ref(false);

    const handleLogin = async () => {
      error.value = '';
      loading.value = true;
      
      try {
        const response = await authAPI.login(credentials.value);
        localStorage.setItem('isAuthenticated', 'true');
        localStorage.setItem('user', JSON.stringify(response.data.user));
        router.push('/dashboard');
      } catch (err) {
        error.value = err.response?.data?.error || 'Login failed. Please try again.';
      } finally {
        loading.value = false;
      }
    };

    return {
      credentials,
      error,
      loading,
      handleLogin
    };
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
}

h1 {
  color: #667eea;
  text-align: center;
  margin-bottom: 0.5rem;
}

h2 {
  color: #333;
  text-align: center;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #667eea;
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary:hover:not(:disabled) {
  background: #5568d3;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #f8d7da;
  border-radius: 5px;
  text-align: center;
}

.register-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.register-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
