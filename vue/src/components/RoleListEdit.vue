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
      <button type="submit" class="btn btn-primary mb-2">Update</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      role: {
        Role_Name: '',
        Description: ''
      },
    };
  },
  created() {
    this.role = this.$route.params.role;
    console.log('Role for editing:', this.role);
  },
  methods: {
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
  },
};
</script>
