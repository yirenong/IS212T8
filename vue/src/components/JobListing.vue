<template>
  <div>
    <h2>Job Listings</h2>
    <ul>
      <li v-for="(job, index) in jobListings" :key="index">
        <!-- <h3>{{ job.Listing_ID  }}</h3> -->
        <p>Job Role: {{ job.Role.Role_Name }}</p>
        <p>Job Description: {{ job.Role.Description }}</p>
        <p>Number of Opening: {{ job.Opening }}</p>
        <p>Date:{{ job.Date_posted }}</p>
        <p>Skills:
          <ul>
            <li v-for="(skill, skillIndex) in job.Role.Skills" :key="skillIndex">
              {{ skill }}
            </li>
          </ul>
        </p>
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
    axios.get('http://localhost:5000/api/job_list')
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


