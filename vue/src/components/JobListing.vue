<template>
  <div class="container mt-4">
    <h2>Job Listings</h2>
    <div class="row mb-4">
      <div class="col-md-4 ">
        <label for="date-select">Sort by: </label>
        <select class="form-control" id="date-select" name="date-select">
          <option value="latest-date">Latest Date</option>
          <option value="oldest-date">Oldest Date</option>
        </select>
      </div>
      <div class="col-md-4">
        <label for="alphabetical-order"></label>
        <div class="form-check">
          <input type="checkbox" class="form-check-input" id="alphabetical-order" name="alphabetical-order">
          <label class="form-check-label" for="alphabetical-order">Ascending Order</label>
        </div>
      </div>
      <div class="col-md-4">
        <label for="input-text"></label>
        <input type="text" class="form-control" id="input-text" name="input-text" placeholder="Seach by Name" v-model="searchbyname">
      </div>
    </div>

    <div v-if="isLoading">
      Loading...
    </div>
    <div v-else>
      <div class="card mb-4" v-for="(job, index) in jobListings" :key="index">
        <div class="row" v-if="job.Role.Role_Name.toLowerCase().includes(searchbyname.toLowerCase()) ">
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
                <b>Skill(s) Required:</b>
              </div>
              <div class="skill-icons">
                <div class="mr-2">
                  <span class="badge bg-success text-white mr-2 p-2" v-for="(skill, skillIndex) in job.Role.Skills"
                    :key="skillIndex">
                    {{ skill }}
                  </span>
                </div>
              </div>
            </div>

            <div class="col-md-6 m-2">
              <b>Skill(s) you have:</b>
              <div class="skill-icons">
                <div class="mr-2">
                  <span class="badge bg-success text-white mr-2 p-2" v-for="skill in staffSkills.Skills" :key="skill">
                    {{ skill }}
                  </span>
                </div>
              </div>
            </div>

            <div class="col-md-6 m-2">
              <b>Skill(s) you don't have:</b>
              <div class="skill-icons">
                <div class="mr-2">
                  <span class="badge bg-danger text-white mr-2 p-2"
                    v-for="skill in leftoverSkills(job.Role.Skills, staffSkills.Skills)" :key="skill">
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
  </div>
</template>

<script>
import axios from 'axios';
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
      isLoading: true,
      searchbyname :'',
    };
  },
  created() {
    if (this.$session.get('user') == null) {
      this.$router.push('/login'); // Redirect to login page
    }
    else {
      this.loadData();
    }

  },
  methods: {
    async loadData() {
      try {
        // Fetch job listings
        const jobListingsResponse = await axios.get('http://localhost:5000/api/job_list');
        this.jobListings = jobListingsResponse.data;
        console.log('Job Listings:', this.jobListings);

        // Fetch user data
        if (this.$session.get('user')) {
          this.userData = this.$session.get('user');
          console.log('User Data:', this.userData);

          // Fetch staff skills
          const staffSkillsResponse = await axios.get(`http://localhost:5000/api/staff_skill/${this.userData.Staff_ID}`);
          this.staffSkills = staffSkillsResponse.data;
          console.log('Staff Skills:', this.staffSkills);
        }

        this.isLoading = false; // Data has been loaded
      } catch (error) {
        console.error('Error fetching data:', error);
        this.isLoading = false; // Set isLoading to false even in case of an error
      }
    },
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
    leftoverSkills(jobSkills, staffSkills) {
      return jobSkills.filter(skill => !staffSkills.includes(skill));
    }
  },
};
</script>
