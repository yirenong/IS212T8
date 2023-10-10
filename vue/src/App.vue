<template>
  <div id="app">
    <AppHeader />
<<<<<<< HEAD
    <RoleCreationModal />
=======
    <!-- <RoleCreationModal /> -->
>>>>>>> 867abc6709267d080f8752ed6db60484647ecd7b
    <!-- Use named views to specify where components should be rendered -->
    <router-view></router-view>
    
    <!-- The footer remains constant -->
    <AppFooter />
  </div>
</template>

<script>
<<<<<<< HEAD
import AppHeader from './components/HeaderComp.vue';
import AppFooter from './components/FooterComp.vue';
import RoleCreationModal from './components/RoleCreationModal.vue';
=======
import AppHeader from "./components/HeaderComp.vue";
import AppFooter from "./components/FooterComp.vue";
//import RoleCreationModal from "./components/RoleCreationModal.vue";
>>>>>>> 867abc6709267d080f8752ed6db60484647ecd7b

export default {
  components: {
    AppHeader,
    AppFooter,
<<<<<<< HEAD
    RoleCreationModal
  },
=======
   // RoleCreationModal,
  }
>>>>>>> 867abc6709267d080f8752ed6db60484647ecd7b
};
</script>
