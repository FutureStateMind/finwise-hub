<template>
  <div class="investments">
    <div class="header">
      <h1>Investment Portfolio</h1>
      <button @click="showModal = true" class="btn-primary">+ Add Investment</button>
    </div>
    
    <div v-if="loading" class="loading">Loading...</div>
    
    <div v-else-if="investments.length === 0" class="empty-state">
      <p>No investments recorded yet. Start tracking your investment portfolio!</p>
    </div>
    
    <div v-else>
      <div class="portfolio-summary">
        <div class="summary-card">
          <h3>Total Invested</h3>
          <p class="amount">${{ totalInvested.toLocaleString() }}</p>
        </div>
        <div class="summary-card">
          <h3>Current Value</h3>
          <p class="amount">${{ currentValue.toLocaleString() }}</p>
        </div>
        <div class="summary-card">
          <h3>Total Profit/Loss</h3>
          <p :class="['amount', profitLoss >= 0 ? 'profit' : 'loss']">
            ${{ profitLoss.toLocaleString() }} ({{ profitLossPercentage.toFixed(2) }}%)
          </p>
        </div>
      </div>
      
      <div class="investments-grid">
        <div v-for="investment in investments" :key="investment.id" class="investment-card">
          <div class="investment-header">
            <h3>{{ investment.investment_name }}</h3>
            <span :class="['risk-badge', investment.risk_level]">{{ investment.risk_level }}</span>
          </div>
          <p class="investment-type">{{ investment.investment_type }}</p>
          <div class="investment-details">
            <div class="detail-row">
              <span>Initial Amount:</span>
              <span>${{ parseFloat(investment.initial_amount).toLocaleString() }}</span>
            </div>
            <div class="detail-row">
              <span>Current Value:</span>
              <span>${{ parseFloat(investment.current_value).toLocaleString() }}</span>
            </div>
            <div class="detail-row">
              <span>Profit/Loss:</span>
              <span :class="investment.profit_loss >= 0 ? 'profit' : 'loss'">
                ${{ parseFloat(investment.profit_loss).toLocaleString() }}
                ({{ parseFloat(investment.profit_loss_percentage).toFixed(2) }}%)
              </span>
            </div>
            <div class="detail-row">
              <span>Purchase Date:</span>
              <span>{{ new Date(investment.purchase_date).toLocaleDateString() }}</span>
            </div>
          </div>
          <div class="investment-actions">
            <button @click="editInvestment(investment)" class="btn-secondary">Edit</button>
            <button @click="deleteInvestment(investment.id)" class="btn-danger">Delete</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal -->
    <div v-if="showModal" class="modal" @click.self="closeModal">
      <div class="modal-content">
        <h2>{{ editing ? 'Edit' : 'Add' }} Investment</h2>
        <form @submit.prevent="saveInvestment">
          <div class="form-group">
            <label>Investment Name *</label>
            <input v-model="formData.investment_name" required />
          </div>
          <div class="form-group">
            <label>Investment Type *</label>
            <select v-model="formData.investment_type" required>
              <option value="stocks">Stocks</option>
              <option value="bonds">Bonds</option>
              <option value="mutual_funds">Mutual Funds</option>
              <option value="etf">ETF</option>
              <option value="real_estate">Real Estate</option>
              <option value="crypto">Cryptocurrency</option>
              <option value="commodities">Commodities</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div class="form-group">
            <label>Risk Level *</label>
            <select v-model="formData.risk_level" required>
              <option value="low">Low Risk</option>
              <option value="medium">Medium Risk</option>
              <option value="high">High Risk</option>
            </select>
          </div>
          <div class="form-group">
            <label>Initial Amount *</label>
            <input type="number" step="0.01" v-model="formData.initial_amount" required />
          </div>
          <div class="form-group">
            <label>Current Value *</label>
            <input type="number" step="0.01" v-model="formData.current_value" required />
          </div>
          <div class="form-group">
            <label>Purchase Date *</label>
            <input type="date" v-model="formData.purchase_date" required />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="formData.description" rows="2"></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn-secondary">Cancel</button>
            <button type="submit" class="btn-primary">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { financeAPI } from '../services/api';

export default {
  name: 'Investments',
  setup() {
    const investments = ref([]);
    const loading = ref(false);
    const showModal = ref(false);
    const editing = ref(null);
    const formData = ref({
      investment_name: '',
      investment_type: 'stocks',
      risk_level: 'medium',
      initial_amount: 0,
      current_value: 0,
      purchase_date: '',
      description: '',
      currency: 'USD'
    });

    const totalInvested = computed(() => 
      investments.value.reduce((sum, inv) => sum + parseFloat(inv.initial_amount || 0), 0)
    );
    
    const currentValue = computed(() => 
      investments.value.reduce((sum, inv) => sum + parseFloat(inv.current_value || 0), 0)
    );
    
    const profitLoss = computed(() => currentValue.value - totalInvested.value);
    
    const profitLossPercentage = computed(() => 
      totalInvested.value > 0 ? (profitLoss.value / totalInvested.value) * 100 : 0
    );

    const fetchInvestments = async () => {
      loading.value = true;
      try {
        const response = await financeAPI.getInvestments();
        investments.value = response.data;
      } catch (error) {
        console.error('Error fetching investments:', error);
      } finally {
        loading.value = false;
      }
    };

    const editInvestment = (investment) => {
      editing.value = investment;
      formData.value = { ...investment };
      showModal.value = true;
    };

    const saveInvestment = async () => {
      try {
        if (editing.value) {
          await financeAPI.updateInvestment(editing.value.id, formData.value);
        } else {
          await financeAPI.createInvestment(formData.value);
        }
        closeModal();
        fetchInvestments();
      } catch (error) {
        console.error('Error saving investment:', error);
        alert('Failed to save investment');
      }
    };

    const deleteInvestment = async (id) => {
      if (confirm('Are you sure you want to delete this investment?')) {
        try {
          await financeAPI.deleteInvestment(id);
          fetchInvestments();
        } catch (error) {
          console.error('Error deleting investment:', error);
        }
      }
    };

    const closeModal = () => {
      showModal.value = false;
      editing.value = null;
      formData.value = {
        investment_name: '',
        investment_type: 'stocks',
        risk_level: 'medium',
        initial_amount: 0,
        current_value: 0,
        purchase_date: '',
        description: '',
        currency: 'USD'
      };
    };

    onMounted(fetchInvestments);

    return {
      investments,
      loading,
      showModal,
      editing,
      formData,
      totalInvested,
      currentValue,
      profitLoss,
      profitLossPercentage,
      editInvestment,
      saveInvestment,
      deleteInvestment,
      closeModal
    };
  }
};
</script>

<style scoped>
.investments {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.loading, .empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.portfolio-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.summary-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.summary-card h3 {
  margin: 0 0 0.5rem 0;
  color: #666;
  font-size: 0.9rem;
  font-weight: 500;
}

.summary-card .amount {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
}

.summary-card .amount.profit {
  color: #28a745;
}

.summary-card .amount.loss {
  color: #dc3545;
}

.investments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.investment-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.investment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.investment-header h3 {
  margin: 0;
  color: #333;
}

.risk-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
}

.risk-badge.low {
  background: #d4edda;
  color: #28a745;
}

.risk-badge.medium {
  background: #fff3cd;
  color: #ffc107;
}

.risk-badge.high {
  background: #f8d7da;
  color: #dc3545;
}

.investment-type {
  color: #666;
  margin: 0.5rem 0 1rem 0;
  text-transform: capitalize;
}

.investment-details {
  margin-bottom: 1rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.detail-row span:first-child {
  color: #666;
}

.detail-row span:last-child {
  font-weight: 600;
  color: #333;
}

.detail-row .profit {
  color: #28a745;
}

.detail-row .loss {
  color: #dc3545;
}

.investment-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn-primary, .btn-secondary, .btn-danger {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5568d3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  flex: 1;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-danger {
  background: #dc3545;
  color: white;
  flex: 1;
}

.btn-danger:hover {
  background: #c82333;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.modal-actions button {
  flex: 1;
}
</style>
