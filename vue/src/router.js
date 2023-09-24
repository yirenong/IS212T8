import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  {
    path: '/job-listing',
    component: () => import('./components/JobListing.vue'),
  },
  {
    path: '/login',
    component: () => import('./components/LoginPage.vue'),
  },
  
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
