<template>
  <div class="container mt-4">
    <h2>Edit Roles</h2>  
    <form @submit.prevent="updateRole">
      <div class="mb-3">
        <label for="Role" class="form-label"><h5>Role:</h5></label>
        <input class="form-control" id="form-control" v-model="role.Role_Name" required>
      </div>
      <div class="mb-3">
        <label for="Description" class="form-label"><h5>Description:</h5></label>
        <input class="form-control" id="form-control" v-model="role.Description" required type="textarea">
      </div>
      <div class="mb-3">
        <label for="Description" class="form-label"><h5>Department:</h5></label>
        <input class="form-control" id="form-control" v-model="role.Department" required type="textarea">
      </div>
      <div class="mb-3">
          <label for="Skills" class="form-label"><h5>Skills:</h5></label> <br>
          <label for="Skills" class="form-label">Current Skills:</label> <br>
          <span v-for="skill in role.Skills" :key="skill.Skill_ID" class="badge bg-secondary">{{ skill }}</span>
          <br><br>
          <label for="Skills" class="form-label">Add Skills:</label> <br>
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
        Department: '',
        Skills: []
      },
      skills: [],
      curr_skills: [],
      unselectedSkills: [],
      selectedSkills: [],
      roleId: null,
    };
  },
  created() {
    const roleId = parseInt(this.$route.params.id, 5);
    console.log("roleID:", roleId);
    axios.get(`http://localhost:5000/api/roles/${roleId}`)
    .then(response => {
      this.role = response.data;
      this.fetchSkills();
      console.log('Role for editing:', this.role);
    })
    .catch(error => {
      console.error('Error fetching role:', error);
    });
    this.skills = this.fetchSkills();
    console.log('Role for editing:', this.role);
    console.log("skills:", this.skills)
    console.log("unselectedSkills:", this.unselectedSkills);
  },
  methods: {
    fetchSkills() {
      return axios.get('http://localhost:5000/api/skill_list')
        .then(response => {
          this.skills = response.data;
          this.unselectedSkills = this.skills.filter(skill => !this.isSkillInRole(skill.Skill_Name));
        })
        .catch(error => {
          console.error('Error fetching skills:', error);
        });
    },
    isSkillInRole(skillName) {
      return this.role.Skills.some(skill => skill === skillName);
    },
    updateRole() {
      if (!this.role.Role_Name || !this.role.Description || !this.role.Department) {
        window.alert('Please fill in all fields.');
        return;
      }

      const updatedRole = {
        Role_Name: this.role.Role_Name,
        Description: this.role.Description,
        Department: this.role.Department,
      };

      axios.put(`http://localhost:5000/api/roles/${this.role.Role_ID}`, updatedRole)
        .then(response => {
          console.log('Role updated successfully:', response.data);

          // Update role skills
          const roleSkillData = {
            role_id: this.role.Role_ID,
            skill_ids: this.selectedSkills
          };
          console.log("roleSkillData:", roleSkillData)
          if (roleSkillData.skill_ids.length !== 0) {
            return axios.post('http://localhost:5000/api/update_role_skills', roleSkillData);
          }
        })
        .then(() => {
          window.alert('Role and role skills updated successfully.');
          //reload page
          window.location.reload();
        })
        .catch(error => {
          console.error('Error updating role and role skills:', error);
        });
    },
    returnToListings() {
      this.$router.push('/hr/role-listing');
    },  
  },
};
</script>