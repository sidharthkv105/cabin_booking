<template>
  <div class="container">
    <div class="box">
      <h2>Dashboard</h2>

      <div class="actions">
        <button @click="goBooking">Book Cabin</button>
        <button class="logout" @click="logout">Logout</button>
      </div>

      <h3>Your Bookings</h3>

      <div v-if="loading" class="empty">Loading...</div>
      <div v-else-if="bookings.length === 0" class="empty">
        No bookings yet
      </div>

      <!-- ✅ Booking cards -->
      <div class="cards">
        <div v-for="b in bookings" :key="b.id" class="card">
          <h4>{{ b.meeting_name }}</h4>

          <p><b>Cabin:</b> {{ getCabinName(b.cabin_id) }}</p>
          <p><b>Date:</b> {{ b.date }}</p>
          <p><b>Time:</b> {{ formatTime(b.from) }} - {{ formatTime(b.to) }}</p>

          <p v-if="b.description" class="note">
            {{ b.description }}
          </p>

          <button class="cancel" @click="cancelBooking(b.id)">
            Cancel
          </button>
        </div>
      </div>
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
const loading = ref(true)

const cabinMap = {
  1: "Cabin A",
  2: "Cabin B",
  3: "Cabin C",
  4: "Cabin D"
}

const getCabinName = (id) => cabinMap[id] || `Cabin ${id}`

const formatTime = (time) => time?.slice(0, 5)

const goBooking = () => router.push("/booking")

const logout = () => {
  localStorage.removeItem("token")
  router.push("/login")
}

onMounted(async () => {
  try {
    const msg = localStorage.getItem("bookingSuccess")
    if (msg) {
      message.value = msg
      localStorage.removeItem("bookingSuccess")
    }

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
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})

const cancelBooking = async (id) => {
  if (!confirm("Cancel this booking?")) return

  await axios.delete(`http://localhost:8000/booking/${id}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`
    }
  })

  bookings.value = bookings.value.filter(b => b.id !== id)
}
</script>

<style>
/* page background */
.container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: start;
  padding-top: 40px;
  background: #f5f5f5;
}

/* main box */
.box {
  width: 400px;
  background: white;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

/* actions */
.actions {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

/* cards container */
.cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* individual card */
.card {
  padding: 12px;
  border-radius: 8px;
  background: #fafafa;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  text-align: left;
}

.card h4 {
  margin-bottom: 5px;
}

/* note */
.note {
  font-size: 13px;
  color: #555;
  margin-top: 5px;
}

/* buttons */
button {
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.logout {
  background: #ddd;
}

.cancel {
  margin-top: 8px;
  background: #f87171;
  color: white;
}

/* empty state */
.empty {
  text-align: center;
  color: #777;
  margin-top: 10px;
}

/* popup */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
}
</style>