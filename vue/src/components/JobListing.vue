<template>
  <div class="container mt-4">
    <h2>Job Listings</h2>
    <table class="table">
    <thead>
      <tr>
        <th>Job Role</th>
        <th>Job Description</th>
        <th>Number of Opening</th>
        <th>Date</th>
        <th>Skills</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(job, index) in jobListings" :key="index">
        <td>{{ job.Role.Role_Name }}</td>
        <td>{{ job.Role.Description }}</td>
        <td>{{ job.Opening }}</td>
        <td>{{ job.Date_posted }}</td>
        <td>
          <ul>
            <li v-for="(skill, skillIndex) in job.Role.Skills" :key="skillIndex">
              {{ skill }}
            </li>
          </ul>
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
};
</script>


