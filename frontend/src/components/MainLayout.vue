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
  margin: 0;           /* ✅ remove outer gap */
  overflow-x: hidden; 
}

body {
  margin: 0;           /* ✅ IMPORTANT */
}

.sidebar {
  width: 200px;
  height: 100vh;          /* ✅ full screen height */
  position: fixed;        /* ✅ lock position */
  top: 0;
  left: 0;

  background: #1f2937;
  color: white;
  padding: 10px;

  overflow: hidden;       /* ✅ no scroll */
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar.collapsed + .content {
  margin-left: 60px;
}

.item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  cursor: pointer;
  border-radius: 6px;
  color: white;
}

.item:hover {
  background: #374151;   /* hover effect */
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

.logout {
  margin-top: auto;
  color: red;
}

/* content */
.content {
  margin-left: 200px;     /* ✅ same as sidebar width */
  padding: 30px;
  background: #f5f6fa;
  min-height: 100vh;
}
</style>