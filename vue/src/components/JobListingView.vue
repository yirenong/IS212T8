<template>
  <div class="container mt-4">
    <h4 class="mb-3">Role Name: {{ jobListing.Role.Role_Name }}</h4>
    <p>
      <span class="me-2">Skills Required: </span>
      <span v-for="(skill, index) in jobListing.Role.Skills" 
            :key="index"
            class="badge bg-secondary me-2">
            {{ skill }}
      </span>
    </p>
    <p class="mb-5">Number of Opening: {{ jobListing.Opening }}</p>
    <p>Number of applications: {{ applications.length }}</p>
    <ul class="list-group mb-3">
      <li v-for="(application, index) in applications"
          :key="index"
          class="list-group-item">
          <div class="float-start">
              <h6>Applicant {{index+1}}: {{ application.Staff_Name }}</h6>
              <div>Applicant Skills: 
                <span v-for="(skill, index) in application.Staff_Skills" 
                        :key="index"
                        class="badge me-2"
                        :class="match(skill) ? 'bg-success' : 'bg-secondary'">
                        {{ skill }}
                  </span>
              </div>
          </div>
          <div class="border bg-light rounded p-2 float-end">
              <p class="m-0">
                Applied in: {{ application.Date.slice(5,16) }} <br>
                Status: {{ application.Status }}
              </p>
          </div>

      </li>
    </ul>
    <button type="submit" class="btn btn-secondary mb-4" @click="returnToListings" >Return to listings</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
        jobListingId: this.$route.params.id,
        jobListing: null,
        applications: []
    };
  },
  created() {
    
    axios.get(`http://localhost:5000/api/job_list/${this.jobListingId}`)
    .then(response => {
      this.jobListing = response.data;
      console.log('Job Listing:', this.jobListing);
    })
    .catch(error => {
      console.error('Error fetching job listings:', error);
    });
    
    axios.get(`http://localhost:5000/api/job_listing/applications/${this.jobListingId}`)  
      .then(response => {
          this.applications = response.data;
          console.log("Applications: ", response.data)
      })
      .catch(error => {
        console.error('Error fetching applicant data:', error)
      })
  },
  methods: {
      match(skill) {
          if ((this.jobListing.Role.Skills).includes(skill)){
              return true
          }
      },
      returnToListings() {
          this.$router.push('/hr/job-listing');
      },
  },
  
};
</script>
