<template>
  <div class="bank-accounts">
    <div class="header">
      <h1>Bank Accounts</h1>
      <button @click="showAddModal = true" class="btn-primary">+ Add Account</button>
    </div>
    
    <div v-if="loading" class="loading">Loading...</div>
    
    <div v-else-if="accounts.length === 0" class="empty-state">
      <p>No bank accounts yet. Add your first account to get started!</p>
    </div>
    
    <div v-else class="accounts-grid">
      <div v-for="account in accounts" :key="account.id" class="account-card">
        <div class="account-header">
          <h3>{{ account.account_name }}</h3>
          <span class="account-type">{{ account.account_type }}</span>
        </div>
        <p class="bank-name">{{ account.bank_name }}</p>
        <p class="balance">${{ parseFloat(account.balance).toLocaleString() }} {{ account.currency }}</p>
        <div class="account-actions">
          <button @click="editAccount(account)" class="btn-secondary">Edit</button>
          <button @click="deleteAccount(account.id)" class="btn-danger">Delete</button>
        </div>
      </div>
    </div>
    
    <!-- Add/Edit Modal -->
    <div v-if="showAddModal" class="modal" @click.self="closeModal">
      <div class="modal-content">
        <h2>{{ editingAccount ? 'Edit' : 'Add' }} Bank Account</h2>
        <form @submit.prevent="saveAccount">
          <div class="form-group">
            <label>Account Name *</label>
            <input v-model="formData.account_name" required />
          </div>
          <div class="form-group">
            <label>Bank Name *</label>
            <input v-model="formData.bank_name" required />
          </div>
          <div class="form-group">
            <label>Account Type *</label>
            <select v-model="formData.account_type" required>
              <option value="savings">Savings</option>
              <option value="checking">Checking</option>
              <option value="credit">Credit Card</option>
              <option value="investment">Investment</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div class="form-group">
            <label>Balance *</label>
            <input type="number" step="0.01" v-model="formData.balance" required />
          </div>
          <div class="form-group">
            <label>Currency</label>
            <input v-model="formData.currency" placeholder="USD" />
          </div>
          <div class="form-group">
            <label>Account Number</label>
            <input v-model="formData.account_number" />
          </div>
          <div class="form-group">
            <label>Notes</label>
            <textarea v-model="formData.notes" rows="3"></textarea>
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
import { ref, onMounted } from 'vue';
import { financeAPI } from '../services/api';

export default {
  name: 'BankAccounts',
  setup() {
    const accounts = ref([]);
    const loading = ref(false);
    const showAddModal = ref(false);
    const editingAccount = ref(null);
    const formData = ref({
      account_name: '',
      bank_name: '',
      account_type: 'savings',
      balance: 0,
      currency: 'USD',
      account_number: '',
      notes: ''
    });

    const fetchAccounts = async () => {
      loading.value = true;
      try {
        const response = await financeAPI.getBankAccounts();
        accounts.value = response.data;
      } catch (error) {
        console.error('Error fetching accounts:', error);
      } finally {
        loading.value = false;
      }
    };

    const editAccount = (account) => {
      editingAccount.value = account;
      formData.value = { ...account };
      showAddModal.value = true;
    };

    const saveAccount = async () => {
      try {
        if (editingAccount.value) {
          await financeAPI.updateBankAccount(editingAccount.value.id, formData.value);
        } else {
          await financeAPI.createBankAccount(formData.value);
        }
        closeModal();
        fetchAccounts();
      } catch (error) {
        console.error('Error saving account:', error);
        alert('Failed to save account');
      }
    };

    const deleteAccount = async (id) => {
      if (confirm('Are you sure you want to delete this account?')) {
        try {
          await financeAPI.deleteBankAccount(id);
          fetchAccounts();
        } catch (error) {
          console.error('Error deleting account:', error);
          alert('Failed to delete account');
        }
      }
    };

    const closeModal = () => {
      showAddModal.value = false;
      editingAccount.value = null;
      formData.value = {
        account_name: '',
        bank_name: '',
        account_type: 'savings',
        balance: 0,
        currency: 'USD',
        account_number: '',
        notes: ''
      };
    };

    onMounted(fetchAccounts);

    return {
      accounts,
      loading,
      showAddModal,
      editingAccount,
      formData,
      editAccount,
      saveAccount,
      deleteAccount,
      closeModal
    };
  }
};
</script>

<style scoped>
.bank-accounts {
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

.accounts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.account-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.account-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.account-header h3 {
  margin: 0;
  color: #333;
}

.account-type {
  background: #667eea;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  text-transform: capitalize;
}

.bank-name {
  color: #666;
  margin: 0.5rem 0;
}

.balance {
  font-size: 1.8rem;
  font-weight: 700;
  color: #28a745;
  margin: 1rem 0;
}

.account-actions {
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
