import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import DataView from '@/views/DataView.vue';
import ImprintView from '@/views/ImprintView.vue';
import GdprView from '@/views/GdprView.vue';

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
  history: createWebHistory(),
  routes,
});

export default router;
