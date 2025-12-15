import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Dashboard from '../views/Dashboard.vue';
import BankAccounts from '../views/BankAccounts.vue';
import Renewals from '../views/Renewals.vue';
import Investments from '../views/Investments.vue';
import AIAdvisor from '../views/AIAdvisor.vue';
import Profile from '../views/Profile.vue';

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { guest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/bank-accounts',
    name: 'BankAccounts',
    component: BankAccounts,
    meta: { requiresAuth: true }
  },
  {
    path: '/renewals',
    name: 'Renewals',
    component: Renewals,
    meta: { requiresAuth: true }
  },
  {
    path: '/investments',
    name: 'Investments',
    component: Investments,
    meta: { requiresAuth: true }
  },
  {
    path: '/ai-advisor',
    name: 'AIAdvisor',
    component: AIAdvisor,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else if (to.meta.guest && isAuthenticated) {
    next('/dashboard');
  } else {
    next();
  }
});

export default router;
