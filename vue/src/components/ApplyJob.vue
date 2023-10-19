<template>
    <div class="container m-2">
      <div class="card">
        <div class="card-header">
          <h2>Job Details</h2>
        </div>
        <div class="card-body">
          <div class="job-info">
            <h4>Title:</h4>
            <p>{{ this.job.Role.Role_Name }}</p>
          </div>
          <div class="job-info">
            <h4>Description:</h4>
            <p>{{ this.job.Role.Description }}</p>
          </div>
          <div class="job-info">
            <h4>Opening:</h4>
            <p>{{ this.job.Opening }}</p>
          </div>
          <div>
            <h4>Skills</h4>
            <ul v-for="skill in this.job.Role.Skills" :key="skill">
                <li>{{ skill }}</li>
            </ul>
          </div>
        </div>
  
        <div class="card-header">
          <h2>User Profile</h2>
        </div>
        <div class="card-body">
          <div class="profile-info">
            <h4>First Name:</h4>
            <p>{{ this.user.Staff_FName }}</p>
          </div>
          <div class="profile-info">
            <h4>Last Name:</h4>
            <p>{{ this.user.Staff_LName }}</p>
          </div>
          <div class="profile-info">
            <h4>Current Department:</h4>
            <p>{{ this.user.Dept }}</p>
          </div>
        </div>
  
        <div class="card-body">
          <button class="btn btn-success" @click="apply">Apply</button>
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
                Role_ID: null,
                Staff_ID: null,
                Status: "Pending",
                Date: null
            }
        };
    },
    created(){
        const id = parseInt(this.$route.params.id, 5);
        console.log("id: ", id);
        if (this.$session.get('user') == null) {
            this.$router.push('/login');
        }
        // else {
        //     this.loadData();
        // }
        this.fetchJob(id);
        this.getUser();
    },
    methods:{
        fetchJob(id){
            axios.get(`http://localhost:5000/api/job_list/${id}`)
            .then(response => {
                this.job = response.data;
                this.application.Role_ID = this.job.Listing_ID;
                console.log('Job:', this.job);
            })
        },
        getUser(){
            this.user = this.$session.get('user');
            this.application.Staff_ID = this.user.Staff_ID; 
            console.log('User Data:', this.user);
        },
        apply(){
            // decrement opening number
            this.application.Date = new Date().toISOString();
            console.log("application: ", this.application)
            axios.post('http://localhost:5000/api/job_listing/apply', this.application)
            .then(response => {
                alert("Application submitted successfully");
                console.log('Application submitted successfully:', response.data);
            })
            .catch(error => {
                console.error('Error submitting application:', error);
            });
        }
    }

}
</script>