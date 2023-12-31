<template>
  <div class="container mt-4">
    <h2>Job Listings</h2>
    <div class="row mb-4">
      <div class="col-md-6 ">
        <label for="date-select">Sort by: </label>
        <select class="form-control form-select" id="date-select" name="date-select" v-model="filterbydate"
          @change="sortbydate">
          <option value="latest">Latest Date</option>
          <option value="oldest">Oldest Date</option>
          <option value="a-z">Alphabetical: A-Z</option>
          <option value="z-a">Alphabetical: Z-A</option>
        </select>
      </div>
      <div class="col-md-6">
        <label for="input-text"></label>
        <input type="text" class="form-control" id="input-text" name="input-text" placeholder="Search by Name"
          v-model="searchbyname">
      </div>
    </div>
    <div class="row mb-4">
      <div class="col-md-4">
        <label for="staffskills-select">Filter by My Skills: </label>
        <select class="form-control form-select" id="staffskills-select" name="staffskills-select"
          @change="buttonskillselection($event)">
          <option value="all" selected="selected">All</option>
          <option v-for="skill in staffSkills.Skills" :key="skill" :value="skill">{{ skill }}</option>
        </select>
      </div>
      <div class="col-md-8">
        <!-- on click of staffskill, it will append button with selected skill name name close icon to remove selection  
            on click of close icon, it will remove skill from filterbystaffskills array
        -->
        <label for="staffskills-select">Selected Skills: </label>
        <br>
        <div class="badge bg-primary text-wrap" v-if="filterbystaffskills.length == 0">Showing All Job Listings</div>
        <button type="button" class="btn btn-primary rounded-pill me-1 " v-for="skill in filterbystaffskills" :key="skill"
          @click="removeSkillselection($event)">
          {{ skill }}
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
    </div>
    <div v-if="isLoading">
      Loading...
    </div>
    <div v-else>
      <transition-group name="staggered-fade" tag="div" v-bind:css="false" v-on:before-enter="beforeEnter"
        v-on:enter="enter" v-on:leave="leave">
        <div v-for="(job) in computedList" :key="job.Listing_ID" class="card shadow mb-4 list-complete-item">
          <div class="row" v-if="job.Role.Role_Name.toLowerCase().includes(searchbyname.toLowerCase())">
            <div class="card-body col-md-8">
              <div class="m-2">
                <h4 class="card-title">{{ job.Role.Role_Name }}</h4>
                <p class="card-text">{{ job.Role.Description }}</p>
              </div>
              <div class="col-md-6">
                <table class="table table-borderless">
                  <tbody>
                    <tr>
                      <td><b>Department:</b></td>
                      <td>{{ job.Role.Department }}</td>
                    </tr>
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
              <hr>
              <div class="m-2">
                <button class="btn btn-success" @click="apply(job.Listing_ID)"
                  :disabled="isRoleAlreadyApplied(job.Listing_ID)">
                  Apply
                </button>
              </div>
            </div>

            <div class="col-md-4">
              <div v-if="job.Role && job.Role.Skills" class="m-2">
                <h4>Match Percentage: {{ calculateMatchPercentage(job.Role.Skills) }}%</h4>
                <DonutChart :percentage="calculateMatchPercentage(job.Role.Skills)" />
              </div>
              <div v-else>
                <b>Match Percentage:</b> Not available
              </div>
            </div>
          </div>
        </div>
      </transition-group>
    </div>
  </div>
</template>
<style>
.list-complete-item {
  transition: all 1s;
}

.list-complete-enter,
.list-complete-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.list-complete-leave-active {
  position: absolute;
}
</style>
<script>
import axios from 'axios';
import velocity from 'velocity-animate'
import DonutChart from './DonutChart.vue';

export default {
  components: {
    DonutChart,
  },

  data() {
    return {
      jobListings: [],
      userData: null,
      staffSkills: [],
      isLoading: true,
      searchbyname: '',
      filterbydate: 'latest',
      sortcheckbox: false,
      appliedRoles: null,
      filterbystaffskills: [],
      filteredjoblistings: [],
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
  computed: {
    // sort computedList by date posted (latest to oldest) or (oldest to latest)
    computedList: function () {
      var vm = this;
      return this.filteredjoblistings.filter(function (item) {
        return item.Role.Role_Name.toLowerCase().indexOf(vm.searchbyname.toLowerCase()) !== -1 &&
          item.Opening > 0;
      })
    }
  },
  methods: {
    async loadData() {
      try {
        // Fetch job listings
        const jobListingsResponse = await axios.get('http://localhost:5000/api/job_list');
        this.jobListings = jobListingsResponse.data;
        this.filteredjoblistings = this.jobListings;
        console.log('Job Listings:', this.jobListings);

        // Fetch user data
        if (this.$session.get('user')) {
          this.userData = this.$session.get('user');
          console.log('User Data:', this.userData);

          const appliedRolesResponse = await axios.get(`http://localhost:5000/api/job_listing/${this.userData.Staff_ID}/applications`);
          this.appliedRoles = appliedRolesResponse.data;
          console.log('Applied Roles:', this.appliedRoles);

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
      if (jobSkills.length === 0) {
        return 100;
      }
      else if (!this.staffSkills || !Array.isArray(this.staffSkills.Skills)) {
        console.error('staffSkills is not valid.');
        return 0;
      }

      else if (!Array.isArray(jobSkills)) {
        console.error('jobSkills is not an array.');
        return 0;
      }
      else {
        const staffSkillsArray = this.staffSkills.Skills;
        const total = jobSkills.length;
        let count = 0;

        for (const skill of staffSkillsArray) {
          if (jobSkills.includes(skill)) {
            count++;
          }
        }

        const percentage = total === 0 ? 0 : (count / total) * 100;
        return Number(percentage.toFixed(2));
      }
    },
    leftoverSkills(jobSkills, staffSkills) {
      return jobSkills.filter(skill => !staffSkills.includes(skill));
    },
    isRoleAlreadyApplied(Listing_ID) {
      // Check if the roleId appears in appliedRoles
      return this.appliedRoles.includes(Listing_ID);
    },
    apply(listing_id) {
      this.$router.push({ name: 'applyJob', params: { id: listing_id } });
    },
    sortbyalphabetical: function () {
      if (this.sortcheckbox == true) {
        this.computedList.sort((a, b) => (a.Role.Role_Name > b.Role.Role_Name) ? 1 : -1)
      }
      else if (this.sortcheckbox == false) {
        this.computedList.sort((a, b) => (a.Role.Role_Name < b.Role.Role_Name) ? 1 : -1)
      }
    },
    sortbydate: function () {
      if (this.filterbydate == 'latest') {
        this.computedList.sort((a, b) => (a.Date_posted < b.Date_posted) ? 1 : -1)
      }
      else if (this.filterbydate == 'oldest') {
        this.computedList.sort((a, b) => (a.Date_posted > b.Date_posted) ? 1 : -1)
      }
      else if (this.filterbydate == 'a-z') {
        this.computedList.sort((a, b) => (a.Role.Role_Name > b.Role.Role_Name) ? 1 : -1)
      }
      else if (this.filterbydate == 'z-a') {
        this.computedList.sort((a, b) => (a.Role.Role_Name < b.Role.Role_Name) ? 1 : -1)
      }
    },
    buttonskillselection: function (event) {
      if (event.target.value == 'all') {
        this.filterbystaffskills = [];
      }
      else {
        if (!this.filterbystaffskills.includes(event.target.value)) {
          this.filterbystaffskills.push(event.target.value);
        }
      }
      // if filterbystaffskills array is not empty, each joblisting must contain all the skills in the filterbystaffskills array
      if (this.filterbystaffskills.length > 0) {
        this.filteredjoblistings = this.jobListings.filter(job => {
          return this.filterbystaffskills.every(skill => job.Role.Skills.includes(skill));
        });
      }
      else {
        this.filteredjoblistings = this.jobListings;
      }
      console.log(this.jobListings)
      


    },
    removeSkillselection: function (event) {
      // remove skill from filterbystaffskills array
      this.filterbystaffskills.splice(this.filterbystaffskills.indexOf(event.target.textContent), 1);
      if (this.filterbystaffskills.length ==0) {
        this.filteredjoblistings = this.jobListings;
      }
    },
    beforeEnter: function (el) {
      el.style.opacity = 0
      el.style.height = 0
    },
    enter: function (el, done) {
      var delay = el.dataset.index * 150
      setTimeout(function () {
        velocity(
          el,
          { opacity: 1, height: '100%' },
          { complete: done }
        )
      }, delay)
    },
    leave: function (el, done) {
      var delay = el.dataset.index * 150
      setTimeout(function () {
        velocity(
          el,
          { opacity: 0, height: 0 },
          { complete: done }
        )
      }, delay)
    }
  },
};
</script>
