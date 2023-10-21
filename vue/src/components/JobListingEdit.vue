<template>
  <div class="container mt-4">
    <h2>Job Listings</h2>
    <table class="table">
      <thead>
        <tr>
          <th>Job Role</th>
          <th>Job Description</th>
          <th>Number of Opening</th>
          <th>Number of Applicants</th>
          <th>Date</th>
          <th>Skills</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(job, index) in jobListings" :key="index">
          <td><router-link :to="'/hr/job-listing/' + job.Listing_ID" class="text-primary nav-link">
            {{ job.Role.Role_Name }}
          </router-link></td>
          <td>{{ job.Role.Description }}</td>
          <td>{{ job.Opening }}</td>
          <td>0</td>
          <td>{{ job.Date_posted }}</td>
          <td>
            <ul>
              <li v-for="(skill, skillIndex) in job.Role.Skills" :key="skillIndex">
                {{ skill }}
              </li>
            </ul>
          </td>
          <td>
            <button class="btn btn-primary" @click="editJobListing(job)">Edit</button>
          </td>
        </tr>
      </tbody>
  </table>
    
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      jobListings: [],
    };
  },
  created() {
    axios.get('http://localhost:5000/api/job_list')
      .then(response => {
        this.jobListings = response.data;
        console.log('Job Listings:', this.jobListings);
      })
      .catch(error => {
        console.error('Error fetching job listings:', error);
      });
  },
  methods: {
    editJobListing(job) {
      this.$router.push({
      name: 'editJobListing',
      params: { job },
    });
    },
  },
  
};
</script>


