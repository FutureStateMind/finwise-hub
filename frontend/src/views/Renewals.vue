<template>
  <div class="renewals">
    <div class="header">
      <h1>Renewals & Subscriptions</h1>
      <button @click="showModal = true" class="btn-primary">+ Add Renewal</button>
    </div>
    
    <div v-if="loading" class="loading">Loading...</div>
    
    <div v-else-if="renewals.length === 0" class="empty-state">
      <p>No renewals tracked yet. Add your subscriptions and renewals to stay on top of them!</p>
    </div>
    
    <div v-else class="renewals-list">
      <div v-for="renewal in renewals" :key="renewal.id" class="renewal-card">
        <div class="renewal-header">
          <h3>{{ renewal.service_name }}</h3>
          <span :class="['status', renewal.is_active ? 'active' : 'inactive']">
            {{ renewal.is_active ? 'Active' : 'Inactive' }}
          </span>
        </div>
        <p class="description">{{ renewal.description }}</p>
        <div class="renewal-details">
          <div class="detail-item">
            <span class="label">Amount:</span>
            <span class="value">${{ parseFloat(renewal.amount).toFixed(2) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Frequency:</span>
            <span class="value">{{ renewal.frequency }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Next Renewal:</span>
            <span class="value">{{ new Date(renewal.next_renewal_date).toLocaleDateString() }}</span>
          </div>
        </div>
        <div class="renewal-actions">
          <button @click="editRenewal(renewal)" class="btn-secondary">Edit</button>
          <button @click="deleteRenewal(renewal.id)" class="btn-danger">Delete</button>
        </div>
      </div>
    </div>
    
    <!-- Modal -->
    <div v-if="showModal" class="modal" @click.self="closeModal">
      <div class="modal-content">
        <h2>{{ editing ? 'Edit' : 'Add' }} Renewal</h2>
        <form @submit.prevent="saveRenewal">
          <div class="form-group">
            <label>Service Name *</label>
            <input v-model="formData.service_name" required />
          </div>
          <div class="form-group">
            <label>Amount *</label>
            <input type="number" step="0.01" v-model="formData.amount" required />
          </div>
          <div class="form-group">
            <label>Frequency *</label>
            <select v-model="formData.frequency" required>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
              <option value="quarterly">Quarterly</option>
              <option value="yearly">Yearly</option>
            </select>
          </div>
          <div class="form-group">
            <label>Next Renewal Date *</label>
            <input type="date" v-model="formData.next_renewal_date" required />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="formData.description" rows="2"></textarea>
          </div>
          <div class="form-group checkbox">
            <label>
              <input type="checkbox" v-model="formData.is_active" />
              Active
            </label>
          </div>
          <div class="form-group checkbox">
            <label>
              <input type="checkbox" v-model="formData.auto_renewal" />
              Auto Renewal
            </label>
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
  name: 'Renewals',
  setup() {
    const renewals = ref([]);
    const loading = ref(false);
    const showModal = ref(false);
    const editing = ref(null);
    const formData = ref({
      service_name: '',
      amount: 0,
      frequency: 'monthly',
      next_renewal_date: '',
      description: '',
      is_active: true,
      auto_renewal: true,
      currency: 'USD'
    });

    const fetchRenewals = async () => {
      loading.value = true;
      try {
        const response = await financeAPI.getRenewals();
        renewals.value = response.data;
      } catch (error) {
        console.error('Error fetching renewals:', error);
      } finally {
        loading.value = false;
      }
    };

    const editRenewal = (renewal) => {
      editing.value = renewal;
      formData.value = { ...renewal };
      showModal.value = true;
    };

    const saveRenewal = async () => {
      try {
        if (editing.value) {
          await financeAPI.updateRenewal(editing.value.id, formData.value);
        } else {
          await financeAPI.createRenewal(formData.value);
        }
        closeModal();
        fetchRenewals();
      } catch (error) {
        console.error('Error saving renewal:', error);
        alert('Failed to save renewal');
      }
    };

    const deleteRenewal = async (id) => {
      if (confirm('Are you sure you want to delete this renewal?')) {
        try {
          await financeAPI.deleteRenewal(id);
          fetchRenewals();
        } catch (error) {
          console.error('Error deleting renewal:', error);
        }
      }
    };

    const closeModal = () => {
      showModal.value = false;
      editing.value = null;
      formData.value = {
        service_name: '',
        amount: 0,
        frequency: 'monthly',
        next_renewal_date: '',
        description: '',
        is_active: true,
        auto_renewal: true,
        currency: 'USD'
      };
    };

    onMounted(fetchRenewals);

    return {
      renewals,
      loading,
      showModal,
      editing,
      formData,
      editRenewal,
      saveRenewal,
      deleteRenewal,
      closeModal
    };
  }
};
</script>

<style scoped>
.renewals {
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

.renewals-list {
  display: grid;
  gap: 1.5rem;
}

.renewal-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.renewal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.renewal-header h3 {
  margin: 0;
  color: #333;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status.active {
  background: #d4edda;
  color: #28a745;
}

.status.inactive {
  background: #f8d7da;
  color: #dc3545;
}

.description {
  color: #666;
  margin: 0.5rem 0 1rem 0;
}

.renewal-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item .label {
  color: #666;
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
}

.detail-item .value {
  color: #333;
  font-weight: 600;
  text-transform: capitalize;
}

.renewal-actions {
  display: flex;
  gap: 0.5rem;
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

.form-group.checkbox label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
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

.form-group.checkbox input {
  width: auto;
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
