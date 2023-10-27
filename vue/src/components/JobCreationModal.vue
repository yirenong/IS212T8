<template>
    <div class="container p-3">
      <h4>Job Creation</h4>
      <hr>
      <form v-if="!submitted" @submit.prevent="createJobListing">
        <!-- Title Field -->
        <div class="title-field mb-3">
          <label for="title" class="col-sm-2 col-form-label">Title</label>
          <div class="select-container mr-5">
            <input class="custom-select mr-3" id="title" v-model="this.formData.title"
                @click="toggleDropdown"
                placeholder="Select Role"
            >
            <ul class="select-options" v-show="showDropdown">
                <li class="select-option"
                    v-for="(role, index) in roles" 
                    :key="index"
                    @click="selectRole(index)">
                    {{ role.Role_Name }}
                </li>
            </ul>
            </div>
        </div>
        <div class="alert alert-danger" v-if="formErrors.title" role="alert">
            {{ formErrors.title }}
        </div>

        <!-- No of Opening Field -->
        <div class="form-group row mb-3">
          <label for="opening" class="col-sm-2 col-form-label">Number of Opening</label>
          <div class="col-sm-3">
            <input v-model="formData.opening" type="number" class="form-control" id="opening" placeholder="Number of Opening">
          </div>
        </div>
        <div class="alert alert-danger" v-if="formErrors.opening" role="alert">
            {{ formErrors.opening }}
        </div>

        <!-- Salary Field -->
        <!-- <div class="form-group row mb-3">
          <label for="salary" class="col-sm-2 col-form-label">Salary</label>
          <div class="col-sm-10">
            <input v-model="formData.salary" type="number" class="form-control" id="salary" placeholder="Salary">
          </div>
        </div>
        <div class="alert alert-danger" v-if="formErrors.salary" role="alert">
            {{ formErrors.salary }}
        </div> -->
  
        <!-- Person of Contact Field -->
        <div class="form-group row my-3">
          <label for="personOfContact" class="col-sm-2 col-form-label">Person Of Contact</label>
          <div class="col-sm-3">
            <input v-model="user.Staff_FName" class="form-control" id="personOfContact" placeholder="Person Of Contact">
          </div>
        </div>
        <div class="form-group row my-3">
          <label for="personOfContact" class="col-sm-2 col-form-label">Contact Email</label>
          <div class="col-sm-3">
            <input v-model="user.Email" class="form-control" id="personOfContact" placeholder="Person Of Contact">
          </div>
        </div>
        <div class="alert alert-danger" v-if="formErrors.personOfContact" role="alert">
            {{ formErrors.personOfContact }}
        </div>

        <!-- Autofilled section -->
        <p>Department: {{ formData.department }}</p>
        <div>
            <p class="d-inline mr-2">Skills Needed:</p> &nbsp;
            <span class="badge bg-success text-white mr-2 p-2 d-inline" v-for="(skill, index) in formData.skills" :key="index">
                {{ skill }}
            </span>
        </div><br>
        <p>Description: {{ formData.description }}</p>

        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
  
      <div v-if="submitted">
        <div class="alert alert-success" role="alert">Job listing created successfully!</div>
        <p>Title: {{ formData.title }}</p>
        <p>Number of Opening: {{ formData.opening }}</p>
        <p>Skills Needed: {{ formData.skills }}</p>
        <p>Person of Contact: {{ formData.personOfContact }}</p>
        <p>Description: {{ formData.description }}</p>
        <p>Date Created: {{ formData.date_created }}</p>
        <!-- <p>Salary: {{ formData.salary }}</p> -->
        <button @click="resetForm" class="btn btn-primary">Create New Job Listing</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        roles: [],
        roleIndex: -1,
        submitted: false,
        formData: {
          title: '',
          opening: 1,
          skills: [],
          personOfContact: 'Jane',  
          description: '',
          department: '',
          date_created: ''
          // salary: ''
        },
        user: null,
        formErrors: {
            title: '',
            personOfContact: '',
            description: ''
            // salary: '',
        },
        showDropdown: false
      };
    },
    created() {
        this.getuser();
        axios.get('http://localhost:5000/api/roles')
            .then(response => {
                this.roles = response.data;
                console.log('Roles:', this.roles);
            })
            .catch(error => {
                console.log('Error fetching roles: ', error);
            })
    },
    methods: {
        getuser(){
            this.user = this.$session.get('user');
            console.log('User Data:', this.user);
        },
        createJobListing() {
            // Reset form errors
            this.formErrors = {
                title: '',
                personOfContact: '',
                description: ''
                // salary: '',
            }
  
            // Form Validation
            this.formErrors.title = this.roleIndex == -1 ? "Please select a role" : ""
            this.formErrors.opening = validateEmpty(this.formData.opening) || validatePositive(this.formData.opening)
            this.formErrors.personOfContact = validateEmpty(this.formData.personOfContact)
            // this.formErrors.salary = validateSalary(this.formData.salary)
            
            // Check if there are any errors
            if (!this.formData.opening){
              console.log("add a number")
            } 
            else if (this.formData.opening <= 0){
              alert("Please enter a valid number of openings")
            }
            else if (this.formErrors.title ||
                this.formErrors.personOfContact ||
                this.formErrors.description
                // this.formErrors.salary ||
            ) 
            {
                console.log("yes")
                return
            }
            else{
              // Creates date
              const currentDate = new Date().toJSON().slice(0,10);
              this.formData.date_created = currentDate;

              const newJob = {
                  Role_ID: this.roles[this.roleIndex].Role_ID,
                  Opening: this.formData.opening,
                  Date_posted: this.formData.date_created
              }

              // Add new job listing to db
              axios.post(`http://localhost:5000/api/job_list/new`, newJob)
              .then(response => {
                  console.log('Job Listing created successfully:', response.data);
                  this.submitted = true;
              })
              .catch(error => {
                  console.error('Error creating new job listing:', error);
              });
            }

        },
        // Functions for dropdown menu
        toggleDropdown() {
            this.showDropdown = !this.showDropdown
        },
        closeDropdown() {
            this.showDropdown = false;
        },
        selectRole(value) {
            this.roleIndex = value
            this.formData.title = this.roles[this.roleIndex].Role_Name
            this.formData.skills = this.roles[this.roleIndex].Skills
            this.formData.description = this.roles[this.roleIndex].Description
            this.formData.department = this.roles[this.roleIndex].Department
            this.showDropdown = false
        },
        // Reset job creation form
        resetForm() {
            this.roleIndex = -1
            this.formData = {
              title: '',
              skills: [],
              opening: 1,
              personOfContact: 'Jane',  
              description: '',
              //salary: '',
            }
            this.submitted = false;
        } 
    }
  };
  
  function validateEmpty(value) {
    if (value == "" || value == null) return "Field cannot be empty."
    return ""
  } 

  function validatePositive(value) {
    return (value < 0) ? "Value has to be positive" : ""
  }
  
  </script>
  
  <style scoped>
  /* Add your CSS styles here */
  .error {
    color: red;
  }
  
  /* Disable number arrows */
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
  
  /* Style skill select field  */
  .select-container {
  position: relative;
  display: inline-block;
  }
  
  .custom-select {
  width: 200px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: 0.3s;
  margin-right: 20px;
  }
  
  .custom-select:focus {
  border:1px solid #67affc;
  box-shadow: 0px 0px 1px 3px #cfe2ff;
  }
  
  .custom-select:focus {
  outline: none;
  }
  
  .select-options {
  position: absolute;
  z-index: 1;
  background-color: #fff;
  border: 1px solid #ccc;
  border-top: none;
  border-radius: 0 0 5px 5px;
  max-height: 150px;
  overflow-y: auto;
  list-style-type: none;
  margin: 0;
  padding: 0;
  }
  
  .select-options.active {
  display: block;
  }
  
  .select-option {
  padding: 10px;
  cursor: pointer;
  }
  
  .select-option:hover {
  background-color: #f0f0f0;
  }
  
  .select-option.highlighted {
  background-color: #007bff;
  color: #fff;
  }
  
  </style>
  