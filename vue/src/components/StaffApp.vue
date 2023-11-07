<template>
  <div class="applications-container">
    <h1 class="title">Staff Applications</h1>
    <div class="application-card" v-for="application in filteredApplications" :key="application.application_id">
      <h3>{{ findRoleByListingId(application.listing_id).role_name }}</h3>
      <p><strong>Description:</strong> {{ findRoleByListingId(application.listing_id).description }}</p>
      <p><strong>Department:</strong> {{ findRoleByListingId(application.listing_id).department }}</p>
      <p><strong>Application Status:</strong> {{ application.status }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      applications: [],
      listings: [],
      roles: [],
      staffId: null
    };
  },
  created() {
    const user = this.$session.get('user');
    if (!user) {
      this.$router.push('/login');
    } else {
      this.staffId = user.Staff_ID;
    }
  },
  computed: {
    filteredApplications() {
      return this.applications.filter(app => app.staff_id === this.staffId);
    }
  },
  methods: {
    findRoleByListingId(id) {
      const listing = this.listings.find(listing => listing.listing_id === id) || {};
      return this.roles.find(role => role.role_id === listing.role_id) || {};
    },
    fetchData() {
      axios.get(`http://localhost:5000/api/staff/staff_app/${this.staffId}`)
        .then(response => {
          this.applications = response.data.applications;
          this.listings = response.data.listings;
          this.roles = response.data.roles;
        });
    }
  },
  mounted() {
    const user = this.$session.get('user');
    if (user && user.Staff_ID) {
      this.staffId = user.Staff_ID;
      this.fetchData();
    }
  }
}
</script>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      applications: [],
      listings: [],
      roles: [],
      staffId: null
    };
  },
  created() {
    const user = this.$session.get('user');
    if (!user) {
      this.$router.push('/login');
    } else {
      this.staffId = user.Staff_ID;
    }
  },
  computed: {
    filteredApplications() {
      return this.applications.filter(app => app.staff_id === this.staffId);
    }
  },
  methods: {
    findRoleByListingId(id) {
      const listing = this.listings.find(listing => listing.listing_id === id) || {};
      return this.roles.find(role => role.role_id === listing.role_id) || {};
    },
    fetchData() {
      axios.get(`http://localhost:5000/api/staff/staff_app/${this.staffId}`)
        .then(response => {
          this.applications = response.data.applications;
          this.listings = response.data.listings;
          this.roles = response.data.roles;
        });
    }
  },
  mounted() {
    const user = this.$session.get('user');
    if (user && user.Staff_ID) {
      this.staffId = user.Staff_ID;
      this.fetchData();
    }
  }
}
</script>

<style scoped>
.applications-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 20px;
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.application-card {
  border: 1px solid #e0e0e0;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 70%;
  max-width: 800px; 
}

.application-card h3 {
  font-size: 1.25rem;
  margin-bottom: 10px;
}

.application-card p {
  margin-bottom: 5px;
}
</style>