<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/" class="logo">💰 FinWise Hub</router-link>
      
      <div class="nav-links">
        <router-link to="/dashboard">Dashboard</router-link>
        <router-link to="/bank-accounts">Bank Accounts</router-link>
        <router-link to="/investments">Investments</router-link>
        <router-link to="/renewals">Renewals</router-link>
        <router-link to="/budget">Budget Planner</router-link>
        <router-link to="/ai-advisor" class="ai-link">AI Advisor</router-link>
      </div>
      
      <div class="nav-actions">
        <router-link to="/profile" class="profile-btn">Profile</router-link>
        <button @click="handleLogout" class="logout-btn">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script>
import { useRouter } from 'vue-router';
import { authAPI } from '../services/api';

export default {
  name: 'Navigation',
  setup() {
    const router = useRouter();

    const handleLogout = async () => {
      try {
        await authAPI.logout();
      } catch (error) {
        console.error('Logout error:', error);
      } finally {
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('user');
        router.push('/login');
      }
    };

    return {
      handleLogout
    };
  }
};
</script>

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  gap: 2rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
  text-decoration: none;
  white-space: nowrap;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  flex: 1;
}

.nav-links a {
  color: #555;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
  white-space: nowrap;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: #667eea;
}

.nav-links .ai-link {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
}

.nav-links .ai-link:hover {
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.nav-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.profile-btn {
  color: #555;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.profile-btn:hover {
  color: #667eea;
}

.logout-btn {
  padding: 0.5rem 1rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.logout-btn:hover {
  background: #c82333;
}

@media (max-width: 968px) {
  .nav-container {
    flex-wrap: wrap;
    padding: 1rem;
  }
  
  .nav-links {
    order: 3;
    width: 100%;
    justify-content: center;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #f0f0f0;
    gap: 1rem;
  }
}

@media (max-width: 600px) {
  .nav-links {
    flex-wrap: wrap;
  }
  
  .nav-links a {
    font-size: 0.9rem;
  }
}
</style>
