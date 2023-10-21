<template>
  <div class="container mt-4">
    <h2>Job Listings</h2>
    <div class="row mb-4">
      <div class="col-md-4 ">
        <label for="date-select">Sort by: </label>
        <select class="form-control" id="date-select" name="date-select" v-model="filterbydate" @change="sortbydate">
          <option value="latest">Latest Date</option>
          <option value="oldest">Oldest Date</option>
        </select>
      </div>
      <div class="col-md-4">
        <label for="alphabetical-order"></label>
        <div class="form-check">
          <input type="checkbox" class="form-check-input" id="alphabetical-order" name="alphabetical-order" v-model="sortcheckbox" @click="sortbyalphabetical">
          <label class="form-check-label" for="alphabetical-order">Alphabetical Order</label>
        </div>
      </div>
      <div class="col-md-4">
        <label for="input-text"></label>
        <input type="text" class="form-control" id="input-text" name="input-text" placeholder="Seach by Name"
          v-model="searchbyname">
      </div>
    </div>

    <div v-if="isLoading">
      Loading...
    </div>
    <div v-else>
      <transition-group name="staggered-fade" tag="div" 
      v-bind:css="false"
    v-on:before-enter="beforeEnter"
    v-on:enter="enter"
    v-on:leave="leave">
        <div v-for="(job) in computedList" :key="job.Listing_ID" class="card mb-4 list-complete-item" >
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
                      <td>{{ job.Role.Department}}</td>
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
                <button class="btn btn-success" @click="apply(job.Role.Role_ID)" :disabled="isRoleAlreadyApplied(job.Role.Role_ID)">
                  Apply
                </button>
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
      </transition-group>
    </div>
  </div>
</template>
<style>
.list-complete-item {
  transition: all 1s;
}
.list-complete-enter, .list-complete-leave-to
 {
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
      staffSkills: null,
      isLoading: true,
      searchbyname: '',
      filterbydate: 'latest',
      sortcheckbox: false,
      appliedRoles: null,
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
  computed:{
    // sort computedList by date posted (latest to oldest) or (oldest to latest)
    computedList: function () {
      var vm = this;
      return this.jobListings.filter(function (item) {
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
    },
    isRoleAlreadyApplied(roleId) {
      // Check if the roleId appears in appliedRoles
      return this.appliedRoles.includes(roleId);
    },
    apply(role_id){
      this.$router.push({ name: 'applyJob', params: { id: role_id } });
    },
    sortbyalphabetical: function(){
      if (this.sortcheckbox == true) {
        this.computedList.sort((a, b) => (a.Role.Role_Name > b.Role.Role_Name) ? 1 : -1)
      }
      else if (this.sortcheckbox == false) {
        this.computedList.sort((a, b) => (a.Role.Role_Name < b.Role.Role_Name) ? 1 : -1)
      }
    },
    sortbydate: function (){
      if (this.filterbydate == 'latest') {
        this.computedList.sort((a, b) => (a.Date_posted < b.Date_posted) ? 1 : -1)
      }
      else if (this.filterbydate == 'oldest') {
        this.computedList.sort((a, b) => (a.Date_posted > b.Date_posted) ? 1 : -1)
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
