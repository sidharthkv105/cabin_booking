<template>
  <div class="home-container">
    <h2>Dashboard</h2>

    <button @click="goBooking">Book Cabin</button>
    <button @click="logout">Logout</button>

    <h3>Your Bookings</h3>

    <div v-if="bookings.length === 0">No bookings yet</div>

    <div v-for="b in bookings" :key="b.id" class="card">
      <p><b>Cabin:</b> {{ b.cabin_id }}</p>
      <p><b>Date:</b> {{ b.date }}</p>
      <p><b>Time:</b> {{ b.from }} - {{ b.to }}</p>
      <button @click="cancelBooking(b.id)">Cancel</button>
    </div>

    <!-- ✅ popup -->
    <div v-if="message" class="overlay">
      <div class="modal">
        <p>{{ message }}</p>
        <button @click="message = ''">OK</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import { useRouter } from "vue-router"

const router = useRouter()
const bookings = ref([])
const message = ref("")

const goBooking = () => router.push("/booking")

const logout = () => {
  localStorage.removeItem("token")
  router.push("/login")
}

onMounted(async () => {
  // ✅ popup message
  const msg = localStorage.getItem("bookingSuccess")
  if (msg) {
    message.value = msg
    localStorage.removeItem("bookingSuccess")
  }

  // ✅ fetch bookings using JWT
  const res = await axios.get("http://localhost:8000/booking/my", {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`
    }
  })

  bookings.value = res.data.map(b => ({
    ...b,
    from: b.start_time,
    to: b.end_time
  }))
})

const cancelBooking = async (id) => {
  await axios.delete(`http://localhost:8000/booking/${id}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`
    }
  })

  bookings.value = bookings.value.filter(b => b.id !== id)
}
</script>

<style>
.home-container { text-align:center; margin-top:50px; }

.card {
  border:1px solid #ddd;
  margin:10px auto;
  padding:10px;
  width:250px;
  border-radius:6px;
}

.overlay {
  position:fixed;
  top:0; left:0;
  width:100%; height:100%;
  background:rgba(0,0,0,0.5);
  display:flex;
  justify-content:center;
  align-items:center;
}

.modal {
  background:white;
  padding:20px;
  border-radius:8px;
}
</style>