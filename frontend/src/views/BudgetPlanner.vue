<template>
  <div class="budget-planner">
    <header class="bp-header">
      <h1>Monthly Budget Planner</h1>
      <p class="subtitle">Allocate your income for a better life with clear rules and subcategories</p>
    </header>

    <section class="bp-controls">
      <label class="field">
        <span>Monthly Income</span>
        <div class="field-input">
          <span class="prefix">{{ currencySymbol }}</span>
          <input
            v-model.number="monthlyIncome"
            type="number"
            min="0"
            step="0.01"
            placeholder="Enter your monthly income"
            @input="coerceIncome"
          />
        </div>
      </label>

      <div class="rule-note" title="Percentages are fixed as per your rule">
        Allocation rule (fixed): Needs 30% · Wishes 10% · Investments 30% · Entertainment 10% · Others 20%
      </div>
    </section>

    <section class="summary" v-if="monthlyIncome > 0">
      <div class="summary-card" v-for="cat in categories" :key="cat.key">
        <div class="summary-header" :style="{ borderColor: cat.color }">
          <div class="summary-title">
            <span class="color-dot" :style="{ background: cat.color }"></span>
            <strong>{{ cat.label }}</strong>
          </div>
          <div class="summary-figures">
            <span class="percent">{{ cat.percent.toFixed(0) }}%</span>
            <span class="amount">{{ formatCurrency(categoryAmount(cat)) }}</span>
          </div>
        </div>

        <div class="subcats">
          <div class="subcat-row header">
            <div class="col-name">Subcategory</div>
            <div class="col-percent">% of {{ cat.label }}</div>
            <div class="col-amount">Amount</div>
            <div class="col-actions"></div>
          </div>

          <div
            class="subcat-row"
            v-for="(sc, idx) in cat.subcategories"
            :key="sc.id"
          >
            <div class="col-name">
              <input
                v-model.trim="sc.name"
                class="input-name"
                type="text"
                :placeholder="`e.g., ${cat.defaults[idx] || 'New item'}`"
                @change="persist"
              />
            </div>
            <div class="col-percent">
              <input
                v-model.number="sc.percent"
                class="input-percent"
                type="number"
                min="0"
                max="100"
                step="0.1"
                @input="normalizePercent(sc, cat)"
              />
            </div>
            <div class="col-amount">
              <span>{{ formatCurrency(subAmount(cat, sc)) }}</span>
            </div>
            <div class="col-actions">
              <button class="btn-link danger" @click="removeSubcat(cat, idx)">Remove</button>
            </div>
          </div>

          <div class="subcat-row footer">
            <div class="col-name">
              <button class="btn add" @click="addSubcat(cat)">+ Add subcategory</button>
            </div>
            <div class="col-percent total" :class="{ invalid: subPercentTotal(cat) !== 100 }">
              Total: {{ subPercentTotal(cat).toFixed(1) }}%
            </div>
            <div class="col-amount total">
              {{ formatCurrency(categoryAmount(cat)) }}
            </div>
            <div class="col-actions"></div>
          </div>

          <p class="validation" v-if="subPercentTotal(cat) !== 100">
            Subcategory percentages should add up to 100%. You're at {{ subPercentTotal(cat).toFixed(1) }}%.
          </p>
        </div>
      </div>
    </section>

    <section v-else class="empty-state">
      <p>Enter your monthly income to see the recommended allocations and define your subcategories.</p>
    </section>

    <section class="export-actions" v-if="monthlyIncome > 0">
      <button class="btn" @click="copyBreakdown">Copy breakdown</button>
      <button class="btn outline" @click="resetAll">Reset</button>
      <span class="copied" v-if="copied">Copied!</span>
    </section>
  </div>
</template>

<script>
export default {
  name: "BudgetPlanner",
  data() {
    return {
      monthlyIncome: null,
      currency: "USD",
      copied: false,
      categories: [
        {
          key: "needs",
          label: "Needs",
          percent: 30,
          color: "#2E86AB",
          defaults: ["Housing", "Groceries", "Utilities", "Transport", "Insurance"],
          subcategories: [
            { id: cryptoRandom(), name: "Housing", percent: 40 },
            { id: cryptoRandom(), name: "Groceries", percent: 25 },
            { id: cryptoRandom(), name: "Utilities", percent: 15 },
            { id: cryptoRandom(), name: "Transport", percent: 10 },
            { id: cryptoRandom(), name: "Insurance", percent: 10 }
          ]
        },
        {
          key: "wishes",
          label: "Wishes",
          percent: 10,
          color: "#7D3C98",
          defaults: ["Dining Out", "Shopping", "Travel"],
          subcategories: [
            { id: cryptoRandom(), name: "Dining Out", percent: 40 },
            { id: cryptoRandom(), name: "Shopping", percent: 35 },
            { id: cryptoRandom(), name: "Travel", percent: 25 }
          ]
        },
        {
          key: "investments",
          label: "Investments",
          percent: 30,
          color: "#239B56",
          defaults: ["Emergency Fund", "Retirement", "Brokerage"],
          subcategories: [
            { id: cryptoRandom(), name: "Emergency Fund", percent: 40 },
            { id: cryptoRandom(), name: "Retirement", percent: 40 },
            { id: cryptoRandom(), name: "Brokerage", percent: 20 }
          ]
        },
        {
          key: "entertainment",
          label: "Entertainment",
          percent: 10,
          color: "#D68910",
          defaults: ["Movies/Shows", "Games", "Events"],
          subcategories: [
            { id: cryptoRandom(), name: "Movies/Shows", percent: 40 },
            { id: cryptoRandom(), name: "Games", percent: 30 },
            { id: cryptoRandom(), name: "Events", percent: 30 }
          ]
        },
        {
          key: "others",
          label: "Others",
          percent: 20,
          color: "#C0392B",
          defaults: ["Gifts", "Charity", "Miscellaneous"],
          subcategories: [
            { id: cryptoRandom(), name: "Gifts", percent: 30 },
            { id: cryptoRandom(), name: "Charity", percent: 30 },
            { id: cryptoRandom(), name: "Miscellaneous", percent: 40 }
          ]
        }
      ]
    };
  },
  computed: {
    currencySymbol() {
      try {
        return (0).toLocaleString(undefined, { style: "currency", currency: this.currency })
          .replace(/[\d\.,\s]/g, "")
          .trim() || "$";
      } catch {
        return "$";
      }
    }
  },
  watch: {
    monthlyIncome: {
      handler() {
        this.persist();
      }
    },
    categories: {
      deep: true,
      handler() {
        this.persist();
      }
    }
  },
  mounted() {
    this.restore();
  },
  methods: {
    coerceIncome() {
      if (this.monthlyIncome === "" || this.monthlyIncome === null || isNaN(this.monthlyIncome)) return;
      if (this.monthlyIncome < 0) this.monthlyIncome = 0;
    },
    categoryAmount(cat) {
      if (!this.monthlyIncome || this.monthlyIncome <= 0) return 0;
      return (this.monthlyIncome * cat.percent) / 100;
    },
    subPercentTotal(cat) {
      return cat.subcategories.reduce((sum, s) => sum + (Number(s.percent) || 0), 0);
    },
    subAmount(cat, sc) {
      const catAmt = this.categoryAmount(cat);
      const pct = Number(sc.percent) || 0;
      return (catAmt * pct) / 100;
    },
    normalizePercent(sc, cat) {
      if (sc.percent < 0) sc.percent = 0;
      if (sc.percent > 100) sc.percent = 100;
      // Do not auto-normalize the rest; instead guide user via validation
      this.persist();
    },
    addSubcat(cat) {
      const remaining = Math.max(0, 100 - this.subPercentTotal(cat));
      cat.subcategories.push({
        id: cryptoRandom(),
        name: "",
        percent: remaining > 0 ? Math.min(remaining, 10) : 0
      });
      this.persist();
    },
    removeSubcat(cat, idx) {
      cat.subcategories.splice(idx, 1);
      this.persist();
    },
    formatCurrency(amount) {
      try {
        return amount.toLocaleString(undefined, {
          style: "currency",
          currency: this.currency,
          minimumFractionDigits: 2,
          maximumFractionDigits: 2
        });
      } catch {
        // Fallback simple formatting
        return `${this.currencySymbol}${Number(amount).toFixed(2)}`;
      }
    },
    copyBreakdown() {
      const lines = [];
      lines.push(`Monthly Income: ${this.formatCurrency(this.monthlyIncome || 0)}`);
      lines.push("");
      this.categories.forEach((cat) => {
        lines.push(`${cat.label} — ${cat.percent}% = ${this.formatCurrency(this.categoryAmount(cat))}`);
        const totalPct = this.subPercentTotal(cat);
        cat.subcategories.forEach((sc) => {
          lines.push(`  - ${sc.name || "Untitled"}: ${Number(sc.percent || 0)}% = ${this.formatCurrency(this.subAmount(cat, sc))}`);
        });
        if (totalPct !== 100) {
          lines.push(`  [!] Subcategories sum to ${totalPct.toFixed(1)}% (should be 100%)`);
        }
        lines.push("");
      });
      const text = lines.join("\n");
      navigator.clipboard.writeText(text).then(() => {
        this.copied = true;
        setTimeout(() => (this.copied = false), 1200);
      });
    },
    resetAll() {
      // Clear local state and storage
      localStorage.removeItem("finwise_budget_v1");
      this.monthlyIncome = null;
      // Reset subcategory percentages to defaults
      this.categories.forEach((c) => {
        const defaults = c.defaults || [];
        c.subcategories = (c.subcategories || []).map((s, i) => ({
          id: cryptoRandom(),
          name: defaults[i] || "",
          percent: s.percent // keep existing unless you'd like to set fixed defaults
        }));
      });
    },
    persist() {
      try {
        const snapshot = {
          monthlyIncome: this.monthlyIncome,
          currency: this.currency,
          categories: this.categories.map((c) => ({
            key: c.key,
            subcategories: c.subcategories.map((s) => ({ id: s.id, name: s.name, percent: s.percent }))
          }))
        };
        localStorage.setItem("finwise_budget_v1", JSON.stringify(snapshot));
      } catch (e) {
        // ignore persistence errors
      }
    },
    restore() {
      try {
        const raw = localStorage.getItem("finwise_budget_v1");
        if (!raw) return;
        const parsed = JSON.parse(raw);
        if (typeof parsed.monthlyIncome === "number") this.monthlyIncome = parsed.monthlyIncome;
        if (parsed.currency) this.currency = parsed.currency;
        if (Array.isArray(parsed.categories)) {
          parsed.categories.forEach((savedCat) => {
            const idx = this.categories.findIndex((c) => c.key === savedCat.key);
            if (idx !== -1 && Array.isArray(savedCat.subcategories)) {
              // Keep fixed category meta (label, percent, color), only restore subcategories
              this.categories[idx].subcategories = savedCat.subcategories.map((s) => ({
                id: s.id || cryptoRandom(),
                name: s.name || "",
                percent: typeof s.percent === "number" ? s.percent : 0
              }));
            }
          });
        }
      } catch (e) {
        // ignore restore errors
      }
    }
  }
};

// Small helper for unique ids without external deps
function cryptoRandom() {
  if (typeof crypto !== "undefined" && crypto.getRandomValues) {
    const buf = new Uint32Array(1);
    crypto.getRandomValues(buf);
    return "id-" + buf[0].toString(36);
  }
  return "id-" + Math.random().toString(36).slice(2);
}
</script>

<style scoped>
.budget-planner {
  max-width: 960px;
  margin: 24px auto 64px;
  padding: 0 16px;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  color: #1e293b;
}

.bp-header h1 {
  margin: 0;
  font-size: 28px;
}
.subtitle {
  margin: 6px 0 0;
  color: #64748b;
}

.bp-controls {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
  margin-top: 16px;
}

.field {
  display: grid;
  gap: 6px;
}
.field-input {
  display: flex;
  align-items: center;
  border: 1px solid #e2e8f0;
  padding: 8px 10px;
  border-radius: 8px;
  background: #fff;
  max-width: 340px;
}
.field-input input {
  border: none;
  outline: none;
  width: 100%;
  font-size: 16px;
}
.field-input .prefix {
  margin-right: 6px;
  color: #64748b;
}

.rule-note {
  font-size: 14px;
  color: #0f766e;
  background: #ecfdf5;
  border: 1px solid #ccfbf1;
  padding: 8px 10px;
  border-radius: 8px;
  display: inline-block;
}

.summary {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  margin-top: 20px;
}

.summary-card {
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  background: #fff;
  overflow: hidden;
}

.summary-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-left: 4px solid;
  padding: 10px 14px;
  background: #f8fafc;
}
.summary-title {
  display: flex;
  align-items: center;
  gap: 8px;
}
.color-dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
}

.summary-figures {
  display: flex;
  align-items: baseline;
  gap: 10px;
}
.summary-figures .percent {
  color: #0ea5e9;
  font-weight: 600;
}
.summary-figures .amount {
  color: #111827;
  font-weight: 700;
}

.subcats {
  padding: 10px 14px 12px;
}
.subcat-row {
  display: grid;
  grid-template-columns: 1.4fr 0.8fr 1fr 0.6fr;
  gap: 10px;
  align-items: center;
  padding: 6px 0;
}
.subcat-row.header {
  color: #64748b;
  font-size: 14px;
  border-bottom: 1px dashed #e2e8f0;
  padding-bottom: 8px;
}
.subcat-row.footer {
  border-top: 1px dashed #e2e8f0;
  margin-top: 6px;
  padding-top: 10px;
}

.input-name, .input-percent {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #e2e8f0;
  padding: 8px 10px;
  border-radius: 8px;
  background: #fff;
  font-size: 14px;
}
.input-percent {
  text-align: right;
}

.col-amount {
  font-weight: 600;
}

.total {
  font-weight: 700;
}
.total.invalid {
  color: #dc2626;
}

.btn {
  background: #0ea5e9;
  color: white;
  border: none;
  padding: 10px 14px;
  border-radius: 8px;
  cursor: pointer;
}
.btn:hover {
  background: #0284c7;
}
.btn.outline {
  background: transparent;
  border: 1px solid #93c5fd;
  color: #0ea5e9;
}
.btn-link {
  background: transparent;
  border: none;
  padding: 6px 8px;
  cursor: pointer;
  color: #2563eb;
}
.btn-link.danger {
  color: #dc2626;
}

.add {
  background: #22c55e;
}
.add:hover {
  background: #16a34a;
}

.empty-state {
  margin-top: 18px;
  color: #64748b;
}

.export-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 18px;
}
.copied {
  color: #16a34a;
}

.validation {
  margin-top: 8px;
  color: #dc2626;
  font-size: 14px;
}

@media (min-width: 860px) {
  .summary {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
