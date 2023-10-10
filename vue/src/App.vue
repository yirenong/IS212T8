<template>
  <div id="app">
    <AppHeader />
    <!-- <RoleCreationModal /> -->
    <!-- Use named views to specify where components should be rendered -->
    <router-view></router-view>
    
    <!-- The footer remains constant -->
    <AppFooter />
  </div>
</template>

<script>
import AppHeader from "./components/HeaderComp.vue";
import AppFooter from "./components/FooterComp.vue";
//import RoleCreationModal from "./components/RoleCreationModal.vue";

export default {
  components: {
    AppHeader,
    AppFooter,
   // RoleCreationModal,
  }
};
</script>
