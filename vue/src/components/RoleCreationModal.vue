<template>
  <div class="container p-3">
    <h4>Role Creation</h4>
    <hr>
    <form v-if="!submitted" @submit.prevent="submitForm">
      <!-- Title Field -->
      <div class="form-group row mb-3">
        <label for="title" class="col-sm-2 col-form-label">Title</label>
        <div class="col-sm-10">
          <input v-model="formData.title" class="form-control" id="title" placeholder="Enter the role name">
        </div>
      </div>
      <div class="alert alert-danger" v-if="formErrors.title" role="alert">
          {{ formErrors.title }}
      </div>

      <!-- Department Field-->
      <div class="form-group row mb-3">
        <label for="department" class="col-sm-2 col-form-label">Department</label>
        <div class="col-sm-10">
          <input v-model="formData.department" class="form-control" id="department" placeholder="Enter the department name">
        </div>
      </div>
      <div class="alert alert-danger" v-if="formErrors.department" role="alert">
          {{ formErrors.department }}
      </div>

      <!-- Skills Field -->
      <div class="skill-field mb-3">
        <label for="skill" class="col-sm-2 col-form-label">Skill</label>
        <div class="select-container mr-5">
          <input class="custom-select mr-3" id="skill" v-model="skillQuery"
              @click="toggleDropdown"
              placeholder="Skill"
          >
          <ul class="select-options" v-show="showDropdown">
              <li class="select-option"
                  v-for="(skill, index) in skill_list" 
                  :key="index"
                  @click="selectSkill(skill.Skill_Name)">
                  {{ skill.Skill_Name }}
              </li>
          </ul>
          <button class="btn btn-secondary" @click.prevent="addSkill">Add</button>
          </div>
      </div>

      <div>
        <p>Skills Needed: </p>
          <ul class="list-group list-group-horizontal">
              <li v-for="(skill, index) in formData.skills"
              :key="index" 
              class="list-group-item badge bg-success text-white">
                {{ skill }}
                  <button @click.prevent="removeSkill(skill)" type="button" class="close bg-transparent border-0" aria-label="Close"><span class="font-weight-bold text-white" aria-hidden="true">&times;</span></button>
              </li>
          </ul>
      </div>
      <div class="alert alert-danger" v-if="formErrors.skills" role="alert">
          {{ formErrors.skills }}
      </div>

      <!-- Description Field -->
      <div class="form-group mb-5">
        <label for="description" class="mb-2">Description</label>
        <textarea v-model="formData.description" class="form-control" id="description" rows="3"></textarea>
      </div>
      <div class="alert alert-danger" v-if="formErrors.description" role="alert">
          {{ formErrors.description }}
      </div>

      <!-- Submit button -->
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>

    <div v-if="submitted">
      <div class="alert alert-success" role="alert">Role created successfully!</div>
      <p>Title: {{ formData.title }}</p>
      <p>Title: {{ formData.department }}</p>
      <div>
        <p class="d-inline mr-2">Skills Needed:</p> &nbsp;
        <span class="badge bg-success text-white mr-2 p-2 d-inline" v-for="(skill, index) in formData.skills" :key="index">
            {{ skill }}
        </span>
    </div>
      <p>Description: {{ formData.description }}</p>
      <button @click="resetForm" class="btn btn-primary">Create New Role</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      formData: {
        title: '',
        skills: [],
        description: '',
        department: '',
      },
      submitted: false,
      formErrors: {
          title: '',
          skills: '',
          description: '',
          department: ''
      },
      skill_list: [],
      skillQuery: '',
      showDropdown: false
    };
  },
  created() {
        axios.get('http://localhost:5000/api/skill_list')
            .then(response => {
                this.skill_list = response.data;
                console.log('Skill List:', this.skill_list);
            })
            .catch(error => {
                console.log('Error fetching skill list: ', error);
            })
    },
  methods: {
      submitForm() {
          // Reset form errors
          this.formErrors = {
              title: '',
              // department: '',
              // // salary: '',
              // personOfContact: '',
              description: ''
          }

          // Form Validation
          this.formErrors.title = validateEmpty(this.formData.title)
          this.formErrors.description = validateEmpty(this.formData.description)
          this.formErrors.department = validateEmpty(this.formData.department)
          this.formErrors.skills = this.formData.skills.length == 0 ? "Skill field cannot be empty" : ""
          
          // Check if there are any errors
          if (this.formErrors.title ||
              this.formErrors.description ||
              this.formErrors.department ||
              this.formErrors.skills 
          ) {
              return
          }

          // Add new role to db
          const newRole = {
                Role_Name: this.formData.title,
                Description: this.formData.description,
                Skills: this.formData.skills,
                Department: this.formData.department,
          }

          axios.post(`http://localhost:5000/api/roles/new`, newRole)
            .then(response => {
                console.log('Role created successfully:', response.data);
                this.submitted = true;
            })
            .catch(error => {
                console.error('Error creating new role:', error);
            });
      },
      toggleDropdown() {
          this.showDropdown = !this.showDropdown
      },
      closeDropdown() {
          this.showDropdown = false;
      },
      selectSkill(value) {
          this.skillQuery = value
          this.showDropdown = false
      },
      addSkill() {
          if (this.skillQuery == ''){
            alert("Please select a skill")
          }
          else if (this.formData.skills.includes(this.skillQuery)){
            alert("Skill already added")
          }
          else{
            this.formData.skills.push(this.skillQuery)
            this.skillQuery = ''
          }
      },
      removeSkill(skill) {
          this.formData.skills = this.formData.skills.filter(s => s != skill)
      },
      resetForm() {
          this.formData = {
            title: '',
            skills: [],
            description: '',
          }
          this.submitted = false;
      } 
  }
};

function validateEmpty(value) {
  if (value == "" || value == null) return "Field cannot be empty."
  return ""
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
