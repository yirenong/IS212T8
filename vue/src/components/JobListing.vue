<template>
  <div>
    <h2>Job Listings</h2>
    <ul>
      <li v-for="(job, index) in jobListings" :key="index">
        <h3>{{ job.Listing_ID  }}</h3>
        <p>{{ job.Role_ID  }}</p>
        <p>{{ job.Opening }}</p>
        <p>{{ job.Date_posted }}</p>
      </li>
    </ul>
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
    axios.get('http://localhost:5000/api/job-listings')
      .then(response => {
        this.jobListings = response.data;
        console.log('Job Listings:', this.jobListings);
      })
      .catch(error => {
        console.error('Error fetching job listings:', error);
      });
  },
};
</script>


