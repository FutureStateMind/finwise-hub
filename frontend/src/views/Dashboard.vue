<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <p class="welcome-message">Welcome back, {{ userName }}!</p>
    
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div class="stat-content">
          <h3>Total Cash</h3>
          <p class="stat-value">${{ totalCash.toLocaleString() }}</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">📈</div>
        <div class="stat-content">
          <h3>Investments</h3>
          <p class="stat-value">${{ totalInvestments.toLocaleString() }}</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🏦</div>
        <div class="stat-content">
          <h3>Bank Accounts</h3>
          <p class="stat-value">{{ bankAccountCount }}</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🔄</div>
        <div class="stat-content">
          <h3>Active Renewals</h3>
          <p class="stat-value">{{ renewalCount }}</p>
        </div>
      </div>
    </div>
    
    <div class="quick-actions">
      <h2>Quick Actions</h2>
      <div class="action-grid">
        <router-link to="/bank-accounts" class="action-btn">
          <span class="action-icon">🏦</span>
          Manage Bank Accounts
        </router-link>
        <router-link to="/investments" class="action-btn">
          <span class="action-icon">📊</span>
          Track Investments
        </router-link>
        <router-link to="/renewals" class="action-btn">
          <span class="action-icon">📅</span>
          View Renewals
        </router-link>
        <router-link to="/ai-advisor" class="action-btn highlight">
          <span class="action-icon">🤖</span>
          AI Financial Advisor
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { financeAPI } from '../services/api';

export default {
  name: 'Dashboard',
  setup() {
    const userName = ref('User');
    const totalCash = ref(0);
    const totalInvestments = ref(0);
    const bankAccountCount = ref(0);
    const renewalCount = ref(0);

    onMounted(async () => {
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      userName.value = user.first_name || user.username || 'User';
      
      try {
        // Fetch bank accounts
        const accountsResponse = await financeAPI.getBankAccounts();
        const accounts = accountsResponse.data;
        bankAccountCount.value = accounts.length;
        totalCash.value = accounts.reduce((sum, acc) => sum + parseFloat(acc.balance || 0), 0);
        
        // Fetch investments
        const investmentsResponse = await financeAPI.getInvestments();
        const investments = investmentsResponse.data;
        totalInvestments.value = investments.reduce((sum, inv) => sum + parseFloat(inv.current_value || 0), 0);
        
        // Fetch renewals
        const renewalsResponse = await financeAPI.getRenewals();
        renewalCount.value = renewalsResponse.data.filter(r => r.is_active).length;
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    });

    return {
      userName,
      totalCash,
      totalInvestments,
      bankAccountCount,
      renewalCount
    };
  }
};
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  color: #333;
  margin-bottom: 0.5rem;
}

.welcome-message {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-content h3 {
  color: #666;
  font-size: 0.9rem;
  margin: 0 0 0.5rem 0;
  font-weight: 500;
}

.stat-value {
  color: #333;
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
}

.quick-actions {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.quick-actions h2 {
  color: #333;
  margin-bottom: 1.5rem;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  text-decoration: none;
  color: #333;
  font-weight: 600;
  transition: all 0.3s;
}

.action-btn:hover {
  background: #e9ecef;
  border-color: #667eea;
  transform: translateY(-2px);
}

.action-btn.highlight {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: #667eea;
}

.action-btn.highlight:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.action-icon {
  font-size: 1.5rem;
}

@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .action-grid {
    grid-template-columns: 1fr;
  }
}
</style>
