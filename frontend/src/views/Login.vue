<template>
  <div class="container">
    <div class="box">
      <h2>Login</h2>

      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />

      <button @click="login">Login</button>

      <p>
        No account?
        <span @click="goSignup">Signup</span>
      </p>

      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import api from "../api"
import { useRouter } from "vue-router"

const router = useRouter()

const username = ref("")
const password = ref("")
const error = ref("")

const goSignup = () => router.push("/signup")

const login = async () => {
  try {
    const res = await api.post("/auth/login", {
      username: username.value,
      password: password.value,
    })

    // ✅ store JWT
    localStorage.setItem("token", res.data.access_token)

    router.push("/dashboard")
  } catch {
    error.value = "Invalid credentials"
  }
}
</script>

<style>
.error { color:red; text-align:center; }
span { cursor:pointer; color:blue; }
</style>