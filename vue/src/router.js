import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  {
    path: '/staff/job-listing',
    component: () => import('./components/JobListing.vue'),
    meta: { allowedRoles: ['Staff'] },
  },
  {
    path: 'staff/job-listing/apply/:id',
    name: 'applyJob',
    component: () => import('./components/ApplyJob.vue'),
    meta: { allowedRoles: ['Staff'] },
  },
  {
    path: '/',
    component: () => import('./components/LoginPage.vue'),
  },
  {
    path: '/hr/searchcandidate',
    component: () => import('./components/SearchCandidate.vue'),
    meta: { allowedRoles: ['HR'] },
  },
  {
    path: '/hr/job-listing',
    component: () => import('./components/JobListingEdit.vue'),
    meta: { allowedRoles: ['HR'] },
  },
  {
    path: '/hr/job-listing/edit/:id',
    name: 'editJobListing',
    component: () => import('./components/JobListingEditIdv.vue'),
    meta: { allowedRoles: ['HR'] },
  },
  {
    path: '/hr/role-listing',
    name: 'rolelisting',
    component: () => import('./components/RoleList.vue'),
    meta: { allowedRoles: ['HR'] },
  },
  {
    path: '/hr/role-listing/edit/:id',
    name: 'editRole',
    component: () => import('./components/RoleListEdit.vue'),
    meta: { allowedRoles: ['HR'] },
  },
  {
    path: '/hr/job-creation', 
    name: 'rolecreation',
    component: () => import('./components/JobCreationModal.vue'),
    meta: { allowedRoles: ['HR'] },
  },
  {
    path: '/hr/role-creation', 
    name: 'rolecreation',
    component: () => import('./components/RoleCreationModal.vue'),
    meta: { allowedRoles: ['HR'] },
  }
  
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

router.beforeEach((to, from, next) => {
  const allowedRoles = to.meta.allowedRoles; // Roles allowed for this route

  // Check if the route has specified allowed roles
  if (allowedRoles) {
    const userRole = sessionStorage.getItem('userRole'); // Get the user role from session storage

    // Check if the user has the allowed role
    if (allowedRoles.includes(userRole)) {
      // User has the allowed role, proceed to the route
      next();
    } else {
      // User does not have the allowed role, redirect to an error page or another appropriate route
      next({ path: '/error', query: { message: 'Access denied.' } });
    }
  } else {
    // No specific roles required for this route, proceed
    next();
  }
});

export default router;