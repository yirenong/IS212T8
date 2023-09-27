<template>
  <div>
    <h2>Job Listings</h2>
    <ul>
      <li v-for="(job, index) in jobListings" :key="index">
        <h3>{{ job.title }}</h3>
        <p>{{ job.description }}</p>
        <p>{{ job.company }}</p>
        <p>{{ job.location }}</p>
        <p>{{ job.posted_date }}</p>
        <p>${{ job.salary }}</p>
        <p>{{ job.contact_email }}</p>
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
