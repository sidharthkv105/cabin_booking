<template>
  <div class="page">

    <!-- HEADER -->
    <div class="topbar">
      <h2>Cabin Booking</h2>
      <button class="primary" @click="goBooking">
        + Book Cabin
      </button>
    </div>

    <!-- CONTENT -->
    <div class="content">

      <!-- UPCOMING -->
      <h3>Upcoming Bookings</h3>

      <div v-if="loading" class="empty">Loading...</div>
      <div v-else-if="upcoming.length === 0" class="empty">
        No upcoming bookings
      </div>

      <div class="cards">
        <div 
          v-for="b in upcoming" 
          :key="b.id" 
          :class="['card', { ongoing: isOngoing(b) }]"
        >

          <div class="card-header">
            <div class="title">
              <h4>{{ b.meeting_name }}</h4>

              <!-- 🔥 ONGOING TAG -->
              <span v-if="isOngoing(b)" class="ongoing-badge">
                ● ONGOING
              </span>
            </div>

            <span class="tag">{{ getCabinName(b.cabin_id) }}</span>
          </div>

          <div class="info">
            <p>📅 {{ b.date }}</p>
            <p>⏰ {{ formatTime(b.from) }} - {{ formatTime(b.to) }}</p>
          </div>

          <p v-if="b.description" class="desc">
            {{ b.description }}
          </p>

          <button class="danger" @click="cancelBooking(b.id)">
            Cancel Booking
          </button>

        </div>
      </div>

      <!-- PAST -->
      <h3 class="past-title">Past Bookings</h3>

      <div v-if="past.length === 0" class="empty">
        No past bookings
      </div>

      <div class="cards">
        <div v-for="b in past" :key="b.id" class="card past">

          <div class="card-header">
            <h4>{{ b.meeting_name }}</h4>
            <span class="tag">{{ getCabinName(b.cabin_id) }}</span>
          </div>

          <div class="info">
            <p>📅 {{ b.date }}</p>
            <p>⏰ {{ formatTime(b.from) }} - {{ formatTime(b.to) }}</p>
          </div>

          <p v-if="b.description" class="desc">
            {{ b.description }}
          </p>

        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import { useRouter } from "vue-router"

const router = useRouter()

const upcoming = ref([])
const past = ref([])
const loading = ref(true)

// cabin mapping
const cabinMap = {
  1: "Cabin A",
  2: "Cabin B",
  3: "Cabin C",
  4: "Cabin D"
}

const getCabinName = (id) => cabinMap[id] || id

const formatTime = (t) => t?.slice(0, 5)
const isOngoing = (b) => {
  if (!b.startTime || !b.endTime) return false

  const now = new Date()
  return b.startTime <= now && b.endTime >= now
}

const goBooking = () => router.push("/booking")

onMounted(async () => {
  try {
    const res = await axios.get("http://localhost:8000/booking/my", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    })

    const now = new Date()

    const formatted = res.data
      .map(b => {
        const start = new Date(`${b.date}T${b.start_time}`)
        const end = new Date(`${b.date}T${b.end_time}`)

        return {
          ...b,
          from: b.start_time,
          to: b.end_time,
          startTime: start,
          endTime: end
        }
      })
      .sort((a, b) => a.startTime - b.startTime)

    upcoming.value = formatted.filter(b => b.endTime >= now)
    past.value = formatted.filter(b => b.endTime < now)

  } catch (err) {
    console.error("API ERROR:", err)
    alert("Failed to load bookings")   // 👈 helps debugging
  } finally {
    loading.value = false   // ✅ ALWAYS runs
  }
})

const cancelBooking = async (id) => {
  if (!confirm("Cancel booking?")) return

  try {
    await axios.delete(`http://localhost:8000/booking/${id}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    })

    upcoming.value = upcoming.value.filter(b => b.id !== id)

  } catch (err) {
    console.error(err)
    alert("Failed to cancel booking")
  }
}
</script>

<style>
.page {
  padding: 30px;
  background: #f5f6fa;
  min-height: 100vh;
}

/* header */
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

/* buttons */
.primary {
  background: #4f46e5;
  color: white;
  padding: 6px 12px;
  font-size: 14px;
  border-radius: 6px;
}

.danger {
  background: #ef4444;
  color: white;
  margin-top: 10px;
  width: 100%;
}

/* layout */
.content {
  width: 100%;
}

/* cards */
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.card {
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.08);
}

.card.past {
  opacity: 0.6;
  background: #f3f4f6;
}

/* card header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tag {
  background: #e0e7ff;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
}

/* info */
.info {
  margin: 10px 0;
}

.desc {
  font-size: 13px;
  color: #555;
}

/* empty */
.empty {
  color: #888;
  margin-bottom: 10px;
}

.past-title {
  margin-top: 30px;
}

/* 🔥 ONGOING CARD STYLE */
.card.ongoing {
  background: #dcfce7;        /* light green */
  border: 2px solid #22c55e;
}
</style>