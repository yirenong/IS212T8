<template>
  <div class="container mt-4">
    <h2>Edit Job</h2>
    <form @submit.prevent="updateJobListing">
      <div class="mb-3">
        <label for="Role" class="form-label">Role</label>
        <select class="form-select" v-model="job.Role.Role_Name">
          <option v-for="role in roles" :key="role.Role_ID" :value="role.Role_Name">{{ role.Role_Name }}</option>
        </select>
      </div>
      <div class="mb-3">
        <label for="Opening" class="form-label">Opening</label>
        <input class="form-control" id="form-control" v-model="job.Opening">
      </div>
      <button type="submit" class="btn btn-primary">Update</button>
    </form>
    <div class="mb-4">
      <button type="submit" class="btn btn-secondary mt-4" @click="returnToListings" >Return to listings</button>
    </div>
    
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      job: null,
      roles: [],
    };
  },
  created() {
    this.job = this.$route.params.job;
    console.log('Job Listing for editing:', this.job);
    this.fetchRoles();
  },
  methods: {
    fetchRoles() {
      axios.get('http://localhost:5000/api/roles')
        .then(response => {
          this.roles = response.data;
        })
        .catch(error => {
          console.error('Error fetching roles:', error);
        });
    },
    updateJobListing() {
      if (!this.job.Role.Role_Name || !this.job.Opening) {
        window.alert('Please fill in all fields.');
        return;
      }

      const updatedJob = {
        Role_Name: this.job.Role.Role_Name,
        Opening: this.job.Opening,
      };


      axios.put(`http://localhost:5000/api/job_list/${this.job.Listing_ID}`, updatedJob)
        .then(response => {
          console.log('Job Listing updated successfully:', response.data);
          window.alert('Job Listing updated successfully.'); 
        })
        .catch(error => {
          console.error('Error updating job listing:', error);
        });
    },
    returnToListings() {
      this.$router.push('/hr/job-listing');
    },
  },
};
</script>
