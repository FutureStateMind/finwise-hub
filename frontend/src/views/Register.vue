<template>
  <div class="register-container">
    <div class="register-card">
      <h1>FinWise Hub</h1>
      <h2>Create Account</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-row">
          <div class="form-group">
            <label for="username">Username *</label>
            <input 
              type="text" 
              id="username" 
              v-model="formData.username" 
              required
              placeholder="Choose a username"
            />
          </div>
          <div class="form-group">
            <label for="email">Email *</label>
            <input 
              type="email" 
              id="email" 
              v-model="formData.email" 
              required
              placeholder="your@email.com"
            />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="first_name">First Name</label>
            <input 
              type="text" 
              id="first_name" 
              v-model="formData.first_name" 
              placeholder="First name"
            />
          </div>
          <div class="form-group">
            <label for="last_name">Last Name</label>
            <input 
              type="text" 
              id="last_name" 
              v-model="formData.last_name" 
              placeholder="Last name"
            />
          </div>
        </div>
        <div class="form-group">
          <label for="password">Password *</label>
          <input 
            type="password" 
            id="password" 
            v-model="formData.password" 
            required
            minlength="8"
            placeholder="At least 8 characters"
          />
        </div>
        <div class="form-group">
          <label for="password_confirm">Confirm Password *</label>
          <input 
            type="password" 
            id="password_confirm" 
            v-model="formData.password_confirm" 
            required
            minlength="8"
            placeholder="Confirm your password"
          />
        </div>
        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="success" class="success-message">{{ success }}</div>
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Creating Account...' : 'Register' }}
        </button>
      </form>
      <p class="login-link">
        Already have an account? <router-link to="/login">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authAPI } from '../services/api';

export default {
  name: 'Register',
  setup() {
    const router = useRouter();
    const formData = ref({
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      password: '',
      password_confirm: ''
    });
    const error = ref('');
    const success = ref('');
    const loading = ref(false);

    const handleRegister = async () => {
      error.value = '';
      success.value = '';
      
      if (formData.value.password !== formData.value.password_confirm) {
        error.value = 'Passwords do not match';
        return;
      }
      
      loading.value = true;
      
      try {
        await authAPI.register(formData.value);
        success.value = 'Account created successfully! Redirecting to login...';
        setTimeout(() => {
          router.push('/login');
        }, 2000);
      } catch (err) {
        if (err.response?.data) {
          const errors = err.response.data;
          error.value = Object.values(errors).flat().join(' ');
        } else {
          error.value = 'Registration failed. Please try again.';
        }
      } finally {
        loading.value = false;
      }
    };

    return {
      formData,
      error,
      success,
      loading,
      handleRegister
    };
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem 1rem;
}

.register-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 600px;
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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

.success-message {
  color: #28a745;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #d4edda;
  border-radius: 5px;
  text-align: center;
}

.login-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.login-link a:hover {
  text-decoration: underline;
}

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
