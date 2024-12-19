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
    meta: {
      title: 'Home',
    },
    component: HomeView,
  },
  {
    path: '/dash1',
    name: 'Dash1',
    component: () => import('@/views/WeatherView.vue'),
  },
  {
    path: '/test',
    name: 'Test',
    component: () => import('@/views/DataView.vue'),
  },
  {
    path: '/dash2_1',
    name: 'Dash2_1',
    component: () => import('@/views/ProtectPublicView.vue'),
  },
  {
    path: '/dash2_2',
    name: 'Dash2_2',
    component: () => import('@/views/ProtectPrivateView.vue'),
  },
  {
    path: '/dash2_3',
    name: 'Dash2_3',
    component: () => import('@/views/GhgView.vue'),
  },
  {
    path: '/dash3',
    name: 'Dash3',
    component: () => import('@/views/AdaptView.vue'),
  },
  {
    path: '/imprint',
    name: 'Imprint',
    component: () => import('@/views/ImprintView.vue'),
  },
  {
    path: '/gdpr',
    name: 'GDPR',
    component: () => import('@/views/GdprView.vue'),
  },
  {
    path: '/detail/:topic?',
    name: 'Detail',
    component: () => import('@/views/DetailView.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // console.log("Scrolling", to, from, savedPosition)
    /*
    if (savedPosition) {
      return savedPosition;
    } else 
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      };
    } else {
      return { top: 0 };
    }
  */
    if (to.hash) {
      console.log("Scrolling to hash", to.hash)
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve({ 
            el: to.hash,
            behavior: 'smooth',
          })
        }, 300)
      })
      /*
      return {
        el: to.hash,
        behavior: 'smooth',
        // above the element
        // top: 30, //150,
      };
      */
    } else {
      if (savedPosition) {
        return savedPosition;
      } else {
        return { top: 0 };
      }
    }
  },
});

// Global navigation guard to close the sidebar on every route transition
router.beforeEach((to, from, next) => {
  // Emit an event or call a method to close the sidebar
  //console.log("Router gard", to, from, next)
  // simple filter here is not enough, because of the params
  let ok = routes.filter((r) => r.path === to.path)
  if (ok.length === 0) {
    // check details
    if ((to.path == "/detail") || (to.path.startsWith('/detail/'))) {
      console.log("Detail page")
      ok = true
    } else {
      alert("404: Redirecting to Home")
      next({ name: 'Home' });
    }
  }

  /*  
  const ok = routes.filter((r) => r.path === to.path)
  */
  if (ok.length === 0) {
    alert("404: Redirecting to Home")
    next({ name: 'Home' });
  }
  document.title = to.meta.title || 'Default Title';
  next()
});



export default router;
