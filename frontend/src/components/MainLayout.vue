<template>
  <div class="layout">
    <!-- Sidebar -->
    <div class="sidebar">
      <div class="menu">
        <div @click="go('/dashboard')" class="item">
          <span>📊</span>
          <span class="text">Dashboard</span>
        </div>

        <div @click="go('/user')" class="item">
          <span>👤</span>
          <span class="text">User</span>
        </div>

        <div @click="logout" class="item logout">
          <span>🚪</span>
          <span class="text">Logout</span>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router"

const router = useRouter()

const go = (path) => router.push(path)

const logout = () => {
  localStorage.removeItem("token")
  router.push("/login")
}
</script>