<template>
  <div class="container mt-4">
    <h2>Edit Roles</h2>  
    <form @submit.prevent="updateRole">
      <div class="mb-3">
        <label for="Role" class="form-label">Role</label>
        <input class="form-control" id="form-control" v-model="role.Role_Name" required>
      </div>
      <div class="mb-3">
        <label for="Description" class="form-label">Description</label>
        <input class="form-control" id="form-control" v-model="role.Description" required type="textarea">
      </div>
      <div class="mb-3">
          <label for="Skills" class="form-label">Skills</label> <br>
          <label for="Skills" class="form-label">Current Skills</label> <br>
          <a v-for="skill in role.Skills" :key="skill.Skill_ID" class="badge bg-secondary">{{ skill }}</a>
          <br>
          <label for="Skills" class="form-label">Add Skills</label> <br>
          <div v-for="skill in unselectedSkills" :key="skill.Skill_ID">
            <label>
              <input type="checkbox" :value="skill.Skill_ID" v-model="selectedSkills" />
              {{ skill.Skill_Name }}
            </label><br />
          </div>
        </div>
      <button type="submit" class="btn btn-primary mb-2">Update</button>
    </form>
    <button type="submit" class="btn btn-secondary mt-4 mb-4" @click="returnToListings" >Return to listings</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      role: {
        Role_Name: '',
        Description: '',
        Skills: []
      },
      skills: [],
      unselectedSkills: [],
      selectedSkills: []
    };
  },
  created() {
    this.role = this.$route.params.role;
    this.skills = this.fetchSkills();
    console.log('Role for editing:', this.role);
    console.log("unselectedSkills:", this.unselectedSkills);
  },
  methods: {
    fetchSkills() {
      return axios.get('http://localhost:5000/api/skill_list')
        .then(response => {
          this.skills = response.data;
          this.unselectedSkills = this.skills.filter(skill => !this.isSkillInRole(skill.Skill_ID));
        })
        .catch(error => {
          console.error('Error fetching skills:', error);
        });
    },
    isSkillInRole(skillId) {
      return this.role.Skills.some(skill => skill.Skill_ID === skillId);
    },
    updateRole() {
      if (!this.role.Role_Name || !this.role.Description) {
        window.alert('Please fill in all fields.');
        return;
      }

      const updatedRole = {
        Role_Name: this.role.Role_Name,
        Description: this.role.Description,
      };

      axios.put(`http://localhost:5000/api/roles/${this.role.Role_ID}`, updatedRole)
        .then(response => {
          console.log('Role updated successfully:', response.data);
          window.alert('Role updated successfully.'); 
        })
        .catch(error => {
          console.error('Error updating role:', error);
        });
    },
    returnToListings() {
      this.$router.push('/hr/role-listing');
    },  
  },
};
</script>