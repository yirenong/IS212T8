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
      <button type="submit" class="btn btn-danger" @click="logout()">Logout</button>
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
        username: '10002',
        password: 'password',
      },
      loginError: null,
    };
  },
  methods: {
    logout() {
      this.$session.destroy()
      this.$router.go(0);
    },
    login() {
      console.log(this.formData)
      axios
        .post('http://localhost:5000/api/login', this.formData)
        .then(response => {
          console.log(response.data); // Log the response message
          //vue set localstorage for response.data
          // this.$cookies.set('user', response.data.Dept);
          this.$session.start()
          this.$session.set('user', response.data);
          this.$router.go(0);
          
          // Redirect or perform actions upon successful login
          // set session storage
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
