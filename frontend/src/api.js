import axios from "axios"
import router from "./router"   // ✅ correct

const api = axios.create({
  baseURL: "http://localhost:8000"
})

api.interceptors.response.use(
  res => res,
  err => {
    if (err.response && err.response.status === 401) {
      localStorage.removeItem("token")
      router.push("/login")
    }
    return Promise.reject(err)
  }
)

export default api