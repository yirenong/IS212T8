<template>
  <div id="app">
    <AppHeader />
    <!-- <RoleCreationModal /> -->
    <!-- Use named views to specify where components should be rendered -->
    <div class=" pb-5">
      <router-view></router-view>
    </div>
    
    
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
