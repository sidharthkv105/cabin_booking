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
import axios from "axios"
import { useRouter } from "vue-router"

const router = useRouter()

const username = ref("")
const password = ref("")
const error = ref("")

const goSignup = () => router.push("/signup")

const login = async () => {
  try {
    const res = await axios.post("http://localhost:8000/auth/login", {
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
.container { display:flex; justify-content:center; align-items:center; height:100vh; background:#f5f5f5; }
.box { width:300px; padding:20px; background:white; border-radius:8px; box-shadow:0 5px 15px rgba(0,0,0,0.1); }
input { display:block; width:100%; margin:10px 0; padding:8px; }
button { width:100%; padding:8px; }
.error { color:red; text-align:center; }
span { cursor:pointer; color:blue; }
</style>