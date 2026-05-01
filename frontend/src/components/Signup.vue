<template>
  <AuthBox title="Signup" :error="error">
    <input v-model="username" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />

    <button @click="signup">Signup</button>

    <template #footer>
      Already have an account?
      <span @click="goLogin">Login</span>
    </template>
  </AuthBox>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"
import { useRouter } from "vue-router"
import AuthBox from "./AuthBox.vue"

const router = useRouter()

const username = ref("")
const password = ref("")
const error = ref("")

const goLogin = () => router.push("/login")

const signup = async () => {
  try {
    await axios.post("http://localhost:8000/auth/signup", {
      username: username.value,
      password: password.value,
    })

    router.push("/login")
  } catch (err) {
    error.value = err.response?.data?.detail || "Signup failed"
  }
}
</script>