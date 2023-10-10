<template>
  <div class="container mt-4">
    <h2>Job Listings</h2>
    <div class="card mb-4" v-for="(job, index) in jobListings" :key="index">
      <div class="row">
        <div class="card-body col-md-8">
          <div class="m-2">
            <h4 class="card-title">{{ job.Role.Role_Name }}</h4>
            <p class="card-text">{{ job.Role.Description }}</p>
          </div>
          <div class="col-md-6">
            <table class="table table-borderless">
              <tbody>
                <tr>
                  <td><b>Number of Openings:</b></td>
                  <td>{{ job.Opening }}</td>
                </tr>
                <tr>
                  <td><b>Date Posted:</b></td>
                  <td>{{ job.Date_posted }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="col-md-6 m-2">
            <div class="mb-2">
              <b>Skill(s):</b>
            </div>
            <div class="skill-icons">
              <div class="mr-2">
                <span
                  class="badge bg-primary text-white mr-2 p-2"
                  v-for="(skill, skillIndex) in job.Role.Skills"
                  :key="skillIndex"
                >
                  {{ skill }}
                </span>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div v-if="job.Role && job.Role.Skills && job.Role.Skills.length > 0" class="m-2">
            <h4>Match Percentage: {{ calculateMatchPercentage(job.Role.Skills) }}%</h4>
              <DonutChart :percentage="calculateMatchPercentage(job.Role.Skills)" />
          </div>
          <div v-else>
            <b>Match Percentage:</b> Not available
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
//import Chart from 'chart.js/auto';
import DonutChart from './DonutChart.vue';

export default {
  components: {
    DonutChart,
  },

  data() {
    return {
      jobListings: [],
      userData: null, 
      staffSkills: null, 
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
  mounted() {
    if (this.$session.get('user')) {
      this.userData = this.$session.get('user');
      console.log('User Data:', this.userData);

      // Make an API call to fetch staff skills based on Staff_ID
      axios.get(`http://localhost:5000/api/staff_skill/${this.userData.Staff_ID}`)
        .then(response => {
          this.staffSkills = response.data;  // Assuming response.data.Skills contains an array of skill IDs
          console.log('Staff Skills:', this.staffSkills);
        })
        .catch(error => {
          console.error('Error fetching staff skills:', error);
        });  
        if (this.$refs.matchChart) {
          this.createMatchPercentageChart();
        }  
    }
  },
  methods: {
    calculateMatchPercentage(jobSkills) {
      if (!this.staffSkills || !Array.isArray(this.staffSkills.Skills)) {
        console.error('staffSkills is not valid.');
        return 0;
      }

      if (!Array.isArray(jobSkills)) {
        console.error('jobSkills is not an array.');
        return 0;
      }

      const staffSkillsArray = this.staffSkills.Skills;
      const total = jobSkills.length;
      let count = 0;

      for (const skill of staffSkillsArray) {
        if (jobSkills.includes(skill)) {
          count++;
        }
      }

      return total === 0 ? 0 : (count / total) * 100;
    },
  
  },
};
</script>
