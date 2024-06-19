import { createRouter, createWebHistory } from 'vue-router';

import HomeView from '@/views/HomeView.vue';
/*
import DataView from '@/views/DataView.vue';
import ImprintView from '@/views/ImprintView.vue';
import GdprView from '@/views/GdprView.vue';
*/ 

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/dash',
    name: 'Dash',
    component: () => import('@/views/DataView.vue'),
  },
  {
    path: '/imprint',
    name: 'Imprint',
    component:  () => import('@/views/ImprintView.vue'),
  },
  {
    path: '/gdpr',
    name: 'GDPR',
    component:  () => import('@/views/GdprView.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      };
    } else {
      return { top: 0 };
    }
  },
});

// Global navigation guard to close the sidebar on every route transition
router.beforeEach((to, from, next) => {
  // Emit an event or call a method to close the sidebar
  console.log("Router gard",to,from,next)
  const ok = routes.filter((r) => r.path === to.path)
  if (ok.length === 0) {
    alert("404: Redirecting to Home")
    next({ name: 'Home' });
  }
  next();
});



export default router;
