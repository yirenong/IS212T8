<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="formData.username" class="form-control"
          placeholder="Enter your username" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="formData.password" class="form-control"
          placeholder="Enter your password" required />
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>
    <div v-if="loginError" class="alert alert-danger mt-3">
      {{ loginError }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      formData: {
        username: '',
        password: '',
      },
      loginError: null,
    };
  },
  methods: {
    login() {
      axios
        .post('http://localhost:5000/login', this.formData)
        .then(response => {
          console.log(response.data.message); // Log the response message
          // Redirect or perform actions upon successful login
        })
        .catch(error => {
          console.error('Error during login:', error);
          this.loginError = 'Invalid username or password. Please try again.';
        });
    },
  },
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.form-group {
  margin-bottom: 15px;
}

.btn-primary {
  width: 100%;
}

.alert {
  margin-top: 10px;
}
</style>
