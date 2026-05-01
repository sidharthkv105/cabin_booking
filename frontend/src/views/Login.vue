<template>
  <div class="login-container">
    <h2>Login</h2>

    <input v-model="username" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />

    <button @click="login">Login</button>

    <p v-if="error" style="color:red">{{ error }}</p>
  </div>
</template>

<script>
import axios from "axios"

export default {
  data() {
    return {
      username: "",
      password: "",
      error: ""
    }
  },
  methods: {
    async login() {
      try {
        const res = await axios.post("http://localhost:8000/auth/login", {
          username: this.username,
          password: this.password
        })

        localStorage.setItem("token", res.data.access_token)

        alert("Login success")
      } catch (err) {
        this.error = "Invalid username or password"
      }
    }
  }
}
</script>

<style>
.login-container {
  width: 300px;
  margin: auto;
  margin-top: 100px;
  text-align: center;
}
input {
  display: block;
  margin: 10px auto;
  padding: 8px;
  width: 100%;
}
button {
  padding: 8px 16px;
}
</style>