<template>
  <div class="container m-2">
    <div class="card">
      <div class="card-header">
        <h2>Job Details</h2>
      </div>
      <div class="card-body">
        <!-- Title -->
        <div class="form-group">
          <label for="title">Title:</label>
          <input type="text" id="title" class="form-control" v-model="job.Role.Role_Name" disabled>
        </div>
        
        <!-- Description -->
        <div class="form-group">
          <label for="description">Description:</label>
          <textarea id="description" class="form-control" v-model="job.Role.Description" disabled></textarea>
        </div>

        <!-- Opening -->
        <div class="form-group">
          <label for="opening">Opening:</label>
          <input type="text" id="opening" class="form-control" v-model="job.Opening" disabled>
        </div>

        <!-- Skills -->
        <div class="form-group">
          <label for="skills">Skills:</label>
          <div>
            <span v-for="skill in job.Role.Skills" :key="skill.Skill_ID" class="badge bg-success text-white p-2">{{ skill }}</span>
          </div>
        </div>
      </div>

      <div class="card-header">
        <h2>User Profile</h2>
      </div>
      <div class="card-body">
        <!-- First Name -->
        <div class="form-group">
          <label for="firstName">First Name:</label>
          <input type="text" id="firstName" class="form-control" v-model="user.Staff_FName" disabled>
        </div>

        <!-- Last Name -->
        <div class="form-group">
          <label for="lastName">Last Name:</label>
          <input type="text" id="lastName" class="form-control" v-model="user.Staff_LName" disabled>
        </div>

        <!-- Current Department -->
        <div class="form-group">
          <label for="department">Current Department:</label>
          <input type="text" id="department" class="form-control" v-model="user.Dept" disabled>
        </div>
      </div>

      <div class="card-body">
        <button class="btn btn-success" @click="apply" :disabled="checkIfApplied(this.id) === true">Apply</button>
      </div>
    </div>
  </div>
</template>
  
  
<script>
import axios from 'axios';
export default {
    data(){
        return{
            id: null,
            job:null,
            user:null,
            application:{
                Listing_ID: null,
                Staff_ID: null,
                Status: "Pending",
                Date: null
            },
            application_list: []
        };
    },
    created(){
        const id = parseInt(this.$route.params.id, 10);
        console.log("id: ", id);
        if (this.$session.get('user') == null) {
            this.$router.push('/login');
        }
        this.fetchJob(id);
        this.getUser();
        if (this.user != null) {
            this.getApplication();
        }
    },
    methods:{
        getApplication(){
            axios.get(`http://localhost:5000/api/job_listing/${this.user.Staff_ID}/applications`)
            .then(response => {
                this.application_list = response.data;
                console.log('Application List:', this.application_list);
            })
        },
        fetchJob(id){
            axios.get(`http://localhost:5000/api/job_list/${id}`)
            .then(response => {
                this.job = response.data;
                this.application.Listing_ID = this.job.Listing_ID;
                console.log('Job:', this.job);
            })
        },
        getUser(){
            this.user = this.$session.get('user');
            this.application.Staff_ID = this.user.Staff_ID; 
            console.log('User Data:', this.user);
        },
        checkIfApplied(id){
          if (id in this.application_list){
            return true;
          }
          else{
            return false;
          }
        },
        apply(){
            this.application.Date = new Date().toISOString();
            console.log("application: ", this.application)
            axios.post('http://localhost:5000/api/job_listing/apply', this.application)
            .then(response => {
                alert(`Application submitted successfully
                      Job Applied: ${ this.job.Role.Role_Name }
                      Date of Application: ${ this.application.Date }
                `);
                console.log('Application submitted successfully:', response.data);
                this.$router.push('/staff/job-listing');
            })
            .catch(error => {
                console.error('Error submitting application:', error);
            });
        }
    }

}
</script>