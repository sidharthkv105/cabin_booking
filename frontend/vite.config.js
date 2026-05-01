import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],

  server: {
    host: true,          // 🔥 allows access from Docker / localhost
    port: 5173,

    watch: {
      usePolling: true   // 🔥 REQUIRED for hot reload inside Docker
    }
  }
})