<template>
  <div class="page">

    <!-- HEADER -->
    <div class="topbar">
      <h2>Cabin Booking</h2>
      <button class="primary" @click="goBooking">
        Book Cabin
      </button>
    </div>

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
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue"
import axios from "axios"
import { useRouter } from "vue-router"

const router = useRouter()

const upcoming = ref([])
const past = ref([])
const loading = ref(true)
const allBookings = ref([])

let interval

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

// 🔥 FETCH BOOKINGS
const fetchBookings = async () => {
  try {
    const res = await axios.get("http://localhost:8000/booking/my", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    })

    allBookings.value = res.data.map(b => {
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

    splitBookings()

  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

// 🔥 SPLIT LOGIC
const splitBookings = () => {
  const now = new Date()

  upcoming.value = allBookings.value.filter(b => b.endTime >= now)
  past.value = allBookings.value.filter(b => b.endTime < now)
}

// 🔥 AUTO UPDATE
onMounted(async () => {
  await fetchBookings()

  interval = setInterval(() => {
    splitBookings()
  }, 60000)
})

onUnmounted(() => {
  clearInterval(interval)
})

// cancel booking
const cancelBooking = async (id) => {
  if (!confirm("Cancel booking?")) return

  try {
    await axios.delete(`http://localhost:8000/booking/${id}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    })

    // update local state
    allBookings.value = allBookings.value.filter(b => b.id !== id)
    splitBookings()

  } catch (err) {
    console.error(err)
    alert("Failed to cancel booking")
  }
}
</script>
