import { createRouter, createWebHistory } from "vue-router"

import Login from "./components/Login.vue"
import Signup from "./components/Signup.vue"
import Home from "./components/Home.vue"
import Booking from "./components/Booking.vue"
import Cabins from "./components/Cabins.vue"

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login },
  { path: "/signup", component: Signup },
  { path: "/dashboard", component: Home },
  { path: "/booking", component: Booking },
  { path: "/cabins", component: Cabins }, 
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const token = localStorage.getItem("token")

  if (to.path === "/dashboard" && !token) {
    return "/login"
  }

  if ((to.path === "/login" || to.path === "/signup") && token) {
    return "/dashboard"
  }
})

export default router