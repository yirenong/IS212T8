<template>
  <div class="container mt-4">
    <h2>List of Roles</h2>  
    <table class="table">
      <thead>
        <tr>
          <th>Role Name</th>
          <th>Description</th>
          <th>Skills</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(role, index) in roles" :key="index">
          <td>{{ role.Role_Name }}</td>
          <td>{{ role.Description }}</td>
          <td>
            <ul>
              <li v-for="(skill, skillIndex) in role.Skills" :key="skillIndex">
                {{ skill }}
              </li>
            </ul>
          </td>
          <td>
            <button class="btn btn-primary" @click="editRole(role)">Edit</button>
          </td>
        </tr>
      </tbody>  
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      roles:[],
    };
  },
  created() {
    axios.get('http://localhost:5000/api/roles')
      .then(response => {
        this.roles = response.data;
        console.log('Roles:', this.roles);
      })
      .catch(error => {
        console.error('Error fetching roles:', error);
      });
  },
  methods: {
    editRole(role) {
      this.$router.push({
        name: 'editRole',
        params: { role: role },
      });
    },
    
  },
};
</script>
