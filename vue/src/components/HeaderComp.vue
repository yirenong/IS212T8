<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <router-link to="/" class="navbar-brand">Job Listing</router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <router-link to="/job-listing" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/login" class="nav-link">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/searchcandidate" class="nav-link">searchcandidates</router-link>
          </li>
          <!-- Add more navigation links as needed -->
        </ul>
      </div>
      <!-- write if for div -->
      <div v-if="$session.get('user') != null">
        <span class="navbar-text">
          Welcome {{ $session.get('user').Staff_FName }}
        </span>
        <button type="submit" class="btn btn-danger" @click="logout()">Logout</button>
      </div>
      
    </nav>
  </template>
  
  <script>
  export default {
    methods: {
      logout() {
        this.$session.destroy()
        this.$router.go(0);
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add your custom styles here */
  </style>
  