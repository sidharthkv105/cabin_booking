<template>
  <div class="layout">
    <!-- Sidebar -->
    <div :class="['sidebar', collapsed ? 'collapsed' : '']">
      <button class="toggle" @click="collapsed = !collapsed">
        ☰
      </button>

      <div class="menu">
        <div @click="go('/dashboard')" class="item">
          <span>📊</span>
          <span v-if="!collapsed">Dashboard</span>
        </div>

        <div @click="go('/user')" class="item">
          <span>👤</span>
          <span v-if="!collapsed">User</span>
        </div>

        <div @click="logout" class="item logout">
          <span>🚪</span>
          <span v-if="!collapsed">Logout</span>
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
import { ref } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()
const collapsed = ref(false)

const go = (path) => router.push(path)

const logout = () => {
  localStorage.removeItem("token")
  router.push("/login")
}
</script>

<style>
.layout {
  display: flex;
  height: 100vh;
}

/* sidebar */
.sidebar {
  width: 200px;
  background: #ffffff;
  box-shadow: 2px 0 10px rgba(0,0,0,0.1);
  padding: 10px;
  transition: 0.3s;
}

.sidebar.collapsed {
  width: 60px;
}

/* toggle button */
.toggle {
  margin-bottom: 20px;
  cursor: pointer;
}

/* menu */
.menu {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  cursor: pointer;
  border-radius: 6px;
}

.item:hover {
  background: #f0f0f0;
}

.logout {
  margin-top: auto;
  color: red;
}

/* content */
.content {
  flex: 1;
  background: #f5f5f5;
  padding: 20px;
}
</style>