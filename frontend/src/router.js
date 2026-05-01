import { createRouter, createWebHistory } from "vue-router"

import MainLayout from "./components/MainLayout.vue"

import Login from "./views/Login.vue"
import Signup from "./views/Signup.vue"

import Home from "./views/Home.vue"
import User from "./views/User.vue"
import Booking from "./views/Booking.vue"
import Cabins from "./views/Cabins.vue"

const routes = [
  { path: "/", redirect: "/dashboard" },

  // 🔒 protected routes
  {
    path: "/",
    component: MainLayout,
    children: [
      { path: "dashboard", component: Home },
      { path: "user", component: User },
      { path: "booking", component: Booking },   // ✅ added
      { path: "cabins", component: Cabins }      // ✅ added
    ]
  },

  // 🔓 public routes
  { path: "/login", component: Login },
  { path: "/signup", component: Signup }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 🔐 auth guard (improved)
router.beforeEach((to) => {
  const token = localStorage.getItem("token")

  const protectedRoutes = ["/dashboard", "/user", "/booking", "/cabins"]

  // if not logged in → redirect to login
  if (protectedRoutes.includes(to.path) && !token) {
    return "/login"
  }

  // if already logged in → prevent going back to login/signup
  if ((to.path === "/login" || to.path === "/signup") && token) {
    return "/dashboard"
  }
})

export default router