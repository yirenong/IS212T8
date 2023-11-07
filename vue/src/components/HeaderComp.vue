<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a v-if="isHR" class="navbar-brand mr-5 p-3">All-In-One</a>
    <a v-else class="navbar-brand mr-5  p-3">All-In-One</a>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ml-auto">
        <!-- Use v-if to conditionally display the "Home" link -->
        <li v-if="isHR" class="nav-item">
          <router-link to="/hr/job-listing" class="nav-link">Home</router-link>
        </li>
        <li v-else class="nav-item">
          <router-link to="/staff/job-listing" class="nav-link">Home</router-link>
        </li>
        <li class="nav-item" v-if="!isAuthenticated">
          <router-link to="/" class="nav-link">Login</router-link>
        </li>
        <li class="nav-item dropdown" v-if="isStaff">
          <router-link to="/staff/profile" class="nav-link">Profile</router-link>
        </li>
        <li class="nav-item dropdown" v-if="isStaff">
          <router-link to="/staff/staff_app" class="nav-link">Applications</router-link>
        </li>
        <li class="nav-item" v-if="isHR">
          <router-link to="/hr/searchcandidate" class="nav-link">Search Candidates</router-link>
        </li>
        <li class="nav-item" v-if="isHR">
          <router-link to="/hr/role-listing" class="nav-link">Role List</router-link>
        </li>
        <li class="nav-item" v-if="isHR">
          <router-link to="/hr/job-creation" class="nav-link">Job Creation</router-link>
        </li>
        <li class="nav-item" v-if="isHR">
          <router-link to="/hr/role-creation" class="nav-link">Role Creation</router-link>
        </li>
        <li class="nav-item" v-if="isHR">
          <router-link to="/hr/skills-creation" class="nav-link">Skill Creation</router-link>
        </li>
      </ul>
    </div>
    <div class="mr-5 p-3" v-if="$session.get('user') != null">
      <span class="navbar-text">
        Welcome {{ $session.get('user').Staff_FName }}
      </span>
      <button type="submit" class="btn btn-danger" @click="logout()">Logout</button>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      isAuthenticated: false,
      user: null,
    };
  },
  mounted() {
    if (this.$session.get('user')) {
      this.isAuthenticated = true;
      this.user = this.$session.get('user');
      console.log(this.$router.currentRoute.path)
      //console.log this.$router.currentRoute.path previous route


      if (this.$session.get('redirect')) {
        this.$session.set('redirect', false);
        if (this.user.Dept === 'HR') {
          this.$router.push('/hr/job-listing'); // Redirect to job listing page
        }
        else {
          this.$router.push('/staff/job-listing'); // Redirect to job listing page
        }
      }


    }
    else {
      if(!this.$session.get('user')) {
      this.$router.push('/'); // Redirect to login page
      }
    }
  },
  computed: {
    isHR() {
      return this.isAuthenticated && this.$session.get('user').Dept === 'HR';
    },
    isStaff() {
      return this.isAuthenticated &&this.$session.get('user').Dept !== 'HR';
    },
  },
  methods: {
    logout() {
      this.$session.destroy();
      this.$router.go(0);
    },
    print() {
      console.log(this.user);
    }
  },
  watch: {
    '$session': {
      handler(val) {
        console.log('Session state changed:', val);
        // Update component data when the session changes
        this.isAuthenticated = !!val.user;
        this.user = val.user;
      },
      deep: true,
    },
    user: {
      handler: function (val) {
        console.log('User variable changed:', val);
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
</style>