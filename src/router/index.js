import { createRouter, createWebHistory } from 'vue-router';

import HomeView from '@/views/HomeView.vue';
import DataView from '@/views/DataView.vue';
import ImprintView from '@/views/ImprintView.vue';
import GdprView from '@/views/GdprView.vue';

import { useConfigStore } from '@/services/configStore';
// const configStore = useConfigStore();

const store = {"instance":null}

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/data',
    name: 'Data',
    component: DataView,
  },
  {
    path: '/imprint',
    name: 'Imprint',
    component: ImprintView,
  },
  {
    path: '/gdpr',
    name: 'GDPR',
    component: GdprView,
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
  next();
});



export default router;
