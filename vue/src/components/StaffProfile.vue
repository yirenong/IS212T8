<template>
    <div class="container mt-4 mb-4 col-lg-8 col-sm-6">
        <div class="card shadow p-4 with-shadow">
            <h4>Profile</h4>
            <hr>
            <div v-if="staff_profile">
                <div class="profile-info">
                    <form>
                        <div class="form-group row mt-3">
                        <label for="name" class="col-sm-4 col-form-label"><strong>Name:</strong></label>
                        <div class="col-sm-8">
                            <input type="text" id="name" class="form-control" :value="staff_profile.Staff_FName + ' ' + staff_profile.Staff_LName" readonly>
                        </div>
                        </div>
                        <div class="form-group row mt-3">
                        <label for="email" class="col-sm-4 col-form-label"><strong>Email:</strong></label>
                        <div class="col-sm-8">
                            <input type="email" id="email" class="form-control" :value="staff_profile.Email" readonly>
                        </div>
                        </div>
                        <div class="form-group row mt-3">
                        <label for="department" class="col-sm-4 col-form-label"><strong>Department:</strong></label>
                        <div class="col-sm-8">
                            <input type="text" id="department" class="form-control" :value="staff_profile.Dept" readonly>
                        </div>
                        </div>
                        <div class="form-group row mt-3">
                        <label for="country" class="col-sm-4 col-form-label"><strong>Country:</strong></label>
                        <div class="col-sm-8">
                            <input type="text" id="country" class="form-control" :value="staff_profile.Country" readonly>
                        </div>
                        </div>
                    </form>
                </div>
                <br>
                <div class="profile-skills">
                    <h5>Skills</h5>
                    <hr>
                    <span v-for="skill in staff_profile.Skills" :key="skill" class="badge text-bg-success p-2">{{ skill }}</span>
                </div>


            </div>
        </div>
    </div>
  </template>
<script>
    import axios from 'axios';

    export default {
        data(){
            return{
                user_id: '',
                staff_profile: null,
            }

        },
        created(){
            if (this.$session.get('user') == null) {
                this.$router.push('/login');
            }
            else {
                let uid = this.$session.get('user');
                this.user_id = uid.Staff_ID;
                console.log("User ID: ", this.user_id);
                this.loadProfile();
            }
        },
        methods:{
            async loadProfile(){
                try{
                    const staffProfileResponse = await axios.get(`http://localhost:5000/api/staff/${this.user_id}`);
                    this.staff_profile = staffProfileResponse.data;
                    console.log('Staff Profile:', this.staff_profile);
                }
                catch(error){
                    console.log(error);
                }
            }

        }


    }
</script>