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
    <p>Number of Applicants: {{ applicants.length }}</p>
    <ul class="list-group mb-3">
      <li v-for="(applicant, index) in applicants"
          :key="index"
          class="list-group-item">
          <div>{{ applicant.name }}</div> <br>
          <div>Applicant Skills: 
            <span v-for="(skill, index) in applicant.skills" 
                    :key="index"
                    class="badge me-2"
                    :class="match(skill) ? 'bg-success' : 'bg-secondary'">
                    {{ skill }}
              </span>
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
        jobListing: null,
        applicants: [
          {
            name: "Candidate 1",
            skills: ['Java']
          },
          {
            name: "Candidate 2",
            skills: ['Python']
          },
          {
            name: "Candidate 3",
            skills: ['Database Management']
          },
          {
            name: "Candidate 4",
            skills: ['Java', 'Python', 'Database Management']
          }
        ]
    };
  },
  created() {
    axios.get(`http://localhost:5000/api/job_list/${this.$route.params.id}`)
      .then(response => {
        this.jobListing = response.data;
        console.log('Job Listing:', this.jobListing);
      })
      .catch(error => {
        console.error('Error fetching job listings:', error);
      });
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
