<template>
  <div class="container">
    <div class="box">
      <h2>SignUp</h2>
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />

      <button @click="signup">Signup</button>

      <p>
        Already have an account?
        <span @click="goLogin">Login</span>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import api from "../api"
import { useRouter } from "vue-router"

// ✅ FIXED IMPORT
import AuthBox from "../components/AuthBox.vue"

const router = useRouter()

const username = ref("")
const password = ref("")
const error = ref("")

const goLogin = () => router.push("/login")

const signup = async () => {
  error.value = ""   // ✅ clear previous error

  if (!username.value || !password.value) {
    error.value = "All fields are required"
    return
  }

  try {
    await api.post("/auth/signup", {
      username: username.value,
      password: password.value,
    })

    router.push("/login")
  } catch (err) {
    error.value = err.response?.data?.detail || "Signup failed"
  }
}
</script>

<style>
.error { color:red; text-align:center; }
span { cursor:pointer; color:blue; }
</style>