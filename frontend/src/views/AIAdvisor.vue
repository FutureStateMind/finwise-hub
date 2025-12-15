<template>
  <div class="ai-advisor">
    <div class="header">
      <h1>🤖 AI Financial Advisor</h1>
      <p class="subtitle">Get personalized recommendations for achieving financial freedom</p>
    </div>
    
    <button @click="fetchAnalysis" class="btn-analyze" :disabled="loading">
      {{ loading ? 'Analyzing...' : '🔄 Refresh Analysis' }}
    </button>
    
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Analyzing your financial data...</p>
    </div>
    
    <div v-else-if="analysis" class="analysis-container">
      <!-- Investment Analysis -->
      <div class="section">
        <h2>📊 Investment Portfolio Analysis</h2>
        <div class="stats-grid">
          <div class="stat-box">
            <span class="stat-label">Total Invested</span>
            <span class="stat-value">${{ analysis.investment_analysis.total_invested.toLocaleString() }}</span>
          </div>
          <div class="stat-box">
            <span class="stat-label">Current Value</span>
            <span class="stat-value">${{ analysis.investment_analysis.current_value.toLocaleString() }}</span>
          </div>
          <div class="stat-box">
            <span class="stat-label">Profit/Loss</span>
            <span :class="['stat-value', analysis.investment_analysis.total_profit_loss >= 0 ? 'profit' : 'loss']">
              ${{ analysis.investment_analysis.total_profit_loss.toLocaleString() }}
            </span>
          </div>
          <div class="stat-box">
            <span class="stat-label">Return</span>
            <span :class="['stat-value', analysis.investment_analysis.profit_loss_percentage >= 0 ? 'profit' : 'loss']">
              {{ analysis.investment_analysis.profit_loss_percentage.toFixed(2) }}%
            </span>
          </div>
        </div>
        
        <div v-if="Object.keys(analysis.investment_analysis.diversification).length > 0" class="subsection">
          <h3>Asset Diversification</h3>
          <div class="diversification-list">
            <div v-for="(data, type) in analysis.investment_analysis.diversification" :key="type" class="diversification-item">
              <span class="type-name">{{ type }}</span>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: data.percentage + '%' }"></div>
              </div>
              <span class="percentage">{{ data.percentage.toFixed(1) }}%</span>
            </div>
          </div>
        </div>
        
        <div v-if="Object.keys(analysis.investment_analysis.risk_profile).length > 0" class="subsection">
          <h3>Risk Profile</h3>
          <div class="risk-list">
            <div v-for="(data, risk) in analysis.investment_analysis.risk_profile" :key="risk" class="risk-item">
              <span :class="['risk-badge', risk.toLowerCase().split(' ')[0]]">{{ risk }}</span>
              <span class="risk-percentage">{{ data.percentage.toFixed(1) }}% of portfolio</span>
              <span class="risk-value">${{ data.total_value.toLocaleString() }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Cash Flow Analysis -->
      <div class="section">
        <h2>💰 Cash Flow & Liquidity</h2>
        <div class="stats-grid">
          <div class="stat-box">
            <span class="stat-label">Total Cash</span>
            <span class="stat-value">${{ analysis.cash_flow_analysis.total_cash.toLocaleString() }}</span>
          </div>
          <div class="stat-box">
            <span class="stat-label">Monthly Expenses</span>
            <span class="stat-value">${{ analysis.cash_flow_analysis.monthly_expenses.toLocaleString() }}</span>
          </div>
          <div class="stat-box">
            <span class="stat-label">Emergency Fund</span>
            <span :class="['stat-value', analysis.cash_flow_analysis.emergency_fund_months >= 3 ? 'good' : 'warning']">
              {{ analysis.cash_flow_analysis.emergency_fund_months.toFixed(1) }} months
            </span>
          </div>
          <div class="stat-box">
            <span class="stat-label">Active Subscriptions</span>
            <span class="stat-value">{{ analysis.cash_flow_analysis.active_subscriptions }}</span>
          </div>
        </div>
      </div>
      
      <!-- AI Recommendations -->
      <div class="section recommendations-section">
        <h2>💡 AI-Powered Recommendations</h2>
        <div class="recommendations-summary">
          <div class="summary-item high">
            <span class="count">{{ analysis.recommendations.summary.high_priority }}</span>
            <span class="label">High Priority</span>
          </div>
          <div class="summary-item medium">
            <span class="count">{{ analysis.recommendations.summary.medium_priority }}</span>
            <span class="label">Medium Priority</span>
          </div>
          <div class="summary-item low">
            <span class="count">{{ analysis.recommendations.summary.low_priority }}</span>
            <span class="label">Low Priority</span>
          </div>
        </div>
        
        <div class="recommendations-list">
          <div v-for="(rec, index) in analysis.recommendations.recommendations" :key="index" 
               :class="['recommendation-card', rec.priority.toLowerCase()]">
            <div class="rec-header">
              <span class="rec-category">{{ rec.category }}</span>
              <span :class="['rec-priority', rec.priority.toLowerCase()]">{{ rec.priority }} Priority</span>
            </div>
            <p class="rec-message">{{ rec.message }}</p>
            <div class="rec-action">
              <strong>Action:</strong> {{ rec.action }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- Action Tasks -->
      <div class="section tasks-section">
        <h2>✅ Your Action Plan</h2>
        <p class="tasks-intro">Follow these steps to achieve financial freedom:</p>
        <div class="tasks-list">
          <div v-for="(task, index) in analysis.recommendations.tasks" :key="index" class="task-item">
            <span class="task-number">{{ index + 1 }}</span>
            <span class="task-text">{{ task }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="empty-state">
      <p>Click "Refresh Analysis" to get your personalized financial recommendations</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { aiAPI } from '../services/api';

export default {
  name: 'AIAdvisor',
  setup() {
    const analysis = ref(null);
    const loading = ref(false);

    const fetchAnalysis = async () => {
      loading.value = true;
      try {
        const response = await aiAPI.getFullAnalysis();
        analysis.value = response.data;
      } catch (error) {
        console.error('Error fetching analysis:', error);
        alert('Failed to fetch analysis. Please try again.');
      } finally {
        loading.value = false;
      }
    };

    onMounted(fetchAnalysis);

    return {
      analysis,
      loading,
      fetchAnalysis
    };
  }
};
</script>

<style scoped>
.ai-advisor {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  color: #333;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
}

.btn-analyze {
  display: block;
  margin: 0 auto 2rem;
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-analyze:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-analyze:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.section {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.section h2 {
  color: #333;
  margin-bottom: 1.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-box {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-label {
  color: #666;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  color: #333;
  font-size: 1.5rem;
  font-weight: 700;
}

.stat-value.profit,
.stat-value.good {
  color: #28a745;
}

.stat-value.loss,
.stat-value.warning {
  color: #dc3545;
}

.subsection {
  margin-top: 2rem;
}

.subsection h3 {
  color: #555;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.diversification-list,
.risk-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.diversification-item {
  display: grid;
  grid-template-columns: 150px 1fr 80px;
  align-items: center;
  gap: 1rem;
}

.type-name {
  font-weight: 600;
  color: #333;
}

.progress-bar {
  height: 20px;
  background: #e9ecef;
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s;
}

.percentage {
  text-align: right;
  font-weight: 600;
  color: #667eea;
}

.risk-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.risk-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
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

.risk-percentage {
  color: #666;
  flex: 1;
}

.risk-value {
  font-weight: 600;
  color: #333;
}

.recommendations-summary {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.summary-item {
  flex: 1;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
}

.summary-item.high {
  background: #f8d7da;
}

.summary-item.medium {
  background: #fff3cd;
}

.summary-item.low {
  background: #d4edda;
}

.summary-item .count {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.summary-item.high .count {
  color: #dc3545;
}

.summary-item.medium .count {
  color: #ffc107;
}

.summary-item.low .count {
  color: #28a745;
}

.summary-item .label {
  color: #666;
  font-size: 0.9rem;
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.recommendation-card {
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid;
}

.recommendation-card.high {
  background: #fff5f5;
  border-color: #dc3545;
}

.recommendation-card.medium {
  background: #fffef5;
  border-color: #ffc107;
}

.recommendation-card.low {
  background: #f5fff5;
  border-color: #28a745;
}

.rec-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.rec-category {
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

.rec-priority {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.rec-priority.high {
  background: #dc3545;
  color: white;
}

.rec-priority.medium {
  background: #ffc107;
  color: #333;
}

.rec-priority.low {
  background: #28a745;
  color: white;
}

.rec-message {
  color: #555;
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.rec-action {
  color: #333;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 5px;
  font-size: 0.9rem;
}

.tasks-intro {
  color: #666;
  margin-bottom: 1.5rem;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.task-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s;
}

.task-item:hover {
  background: #e9ecef;
  transform: translateX(5px);
}

.task-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background: #667eea;
  color: white;
  border-radius: 50%;
  font-weight: 700;
  flex-shrink: 0;
}

.task-text {
  color: #333;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .ai-advisor {
    padding: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .diversification-item {
    grid-template-columns: 100px 1fr 60px;
  }
  
  .recommendations-summary {
    flex-direction: column;
  }
}
</style>
