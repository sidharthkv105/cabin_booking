import { createRouter, createWebHistory } from "vue-router"
import User from "./views/User.vue"
import MainLayout from "./components/MainLayout.vue"
import Login from "./views/Login.vue"
import Signup from "./views/Signup.vue"
import Home from "./views/Home.vue"
import Booking from "./views/Booking.vue"
import Cabins from "./views/Cabins.vue"

const routes = [
  { path: "/", redirect: "/dashboard" },

  {
    path: "/",
    component: MainLayout,
    children: [
      { path: "dashboard", component: Home },
      { path: "user", component: User }
    ]
  },

  { path: "/login", component: Login },
  { path: "/signup", component: Signup }
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