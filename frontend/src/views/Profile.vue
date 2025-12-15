<template>
  <div class="profile">
    <h1>Profile</h1>
    
    <div v-if="loading" class="loading">Loading...</div>
    
    <div v-else class="profile-content">
      <form @submit.prevent="saveProfile" class="profile-form">
        <div class="form-section">
          <h2>Personal Information</h2>
          <div class="form-group">
            <label>Phone Number</label>
            <input v-model="profileData.phone_number" type="tel" />
          </div>
          <div class="form-group">
            <label>Date of Birth</label>
            <input v-model="profileData.date_of_birth" type="date" />
          </div>
          <div class="form-group">
            <label>Occupation</label>
            <input v-model="profileData.occupation" />
          </div>
          <div class="form-group">
            <label>Address</label>
            <textarea v-model="profileData.address" rows="3"></textarea>
          </div>
        </div>
        
        <div class="form-section">
          <h2>Financial Information</h2>
          <div class="form-group">
            <label>Annual Income</label>
            <input v-model="profileData.annual_income" type="number" step="0.01" />
          </div>
          <div class="form-group">
            <label>Financial Goals</label>
            <textarea v-model="profileData.financial_goals" rows="5" 
                      placeholder="Describe your financial goals and objectives..."></textarea>
          </div>
        </div>
        
        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="success" class="success-message">{{ success }}</div>
        
        <button type="submit" class="btn-primary" :disabled="saving">
          {{ saving ? 'Saving...' : 'Save Profile' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { authAPI } from '../services/api';

export default {
  name: 'Profile',
  setup() {
    const profileData = ref({
      phone_number: '',
      date_of_birth: '',
      address: '',
      occupation: '',
      annual_income: '',
      financial_goals: ''
    });
    const loading = ref(false);
    const saving = ref(false);
    const error = ref('');
    const success = ref('');

    const fetchProfile = async () => {
      loading.value = true;
      try {
        const response = await authAPI.getProfile();
        Object.assign(profileData.value, response.data);
      } catch (err) {
        console.error('Error fetching profile:', err);
      } finally {
        loading.value = false;
      }
    };

    const saveProfile = async () => {
      error.value = '';
      success.value = '';
      saving.value = true;
      
      try {
        await authAPI.updateProfile(profileData.value);
        success.value = 'Profile updated successfully!';
        setTimeout(() => {
          success.value = '';
        }, 3000);
      } catch (err) {
        error.value = 'Failed to update profile. Please try again.';
      } finally {
        saving.value = false;
      }
    };

    onMounted(fetchProfile);

    return {
      profileData,
      loading,
      saving,
      error,
      success,
      saveProfile
    };
  }
};
</script>

<style scoped>
.profile {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  color: #333;
  margin-bottom: 2rem;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.profile-content {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 2rem;
}

.form-section h2 {
  color: #555;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus {
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
</style>
