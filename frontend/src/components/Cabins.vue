<template>
  <div class="container">
    <h2>Select Cabin</h2>

    <div class="grid">
      <div
        v-for="cabin in cabins"
        :key="cabin.id"
        :class="['cabin', cabin.booked ? 'booked' : 'available']"
        @click="selectCabin(cabin)"
      >
        {{ cabin.name }}
      </div>
    </div>

    <!-- ✅ Meeting Form -->
    <div v-if="selected" class="form-box">
      <h3>Meeting Details</h3>

      <input
        v-model="meetingName"
        placeholder="Meeting name"
      />

      <textarea
        v-model="description"
        placeholder="Description (optional)"
      ></textarea>

      <button @click="confirmBooking">
        Confirm Booking ({{ selected.name }})
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import { useRoute, useRouter } from "vue-router"

const route = useRoute()
const router = useRouter()

const cabins = ref([])
const selected = ref(null)

const meetingName = ref("")
const description = ref("")

const date = route.query.date
const from = route.query.from
const to = route.query.to

onMounted(async () => {
  const res = await axios.get("http://localhost:8000/booking/availability", {
    params: { date, from_time: from, to_time: to }
  })

  cabins.value = res.data
})

const selectCabin = (cabin) => {
  if (!cabin.booked) {
    selected.value = cabin
  }
}

const confirmBooking = async () => {
  if (!meetingName.value) {
    alert("Meeting name is required")
    return
  }

  await axios.post(
    "http://localhost:8000/booking",
    {
      cabin_id: selected.value.id,
      date,
      from_time: from,
      to_time: to,
      meeting_name: meetingName.value,     // ✅ added
      description: description.value       // ✅ added
    },
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    }
  )

  localStorage.setItem(
    "bookingSuccess",
    `Meeting "${meetingName.value}" booked in ${selected.value.name}`
  )

  router.push("/dashboard")
}
</script>

<style>
.container {
  text-align: center;
  margin-top: 40px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, 120px);
  gap: 10px;
  justify-content: center;
  margin-top: 20px;
}

.cabin {
  padding: 20px;
  text-align: center;
  border-radius: 6px;
  cursor: pointer;
}

.available {
  background: #d1fae5;
}

.booked {
  background: #fecaca;
  cursor: not-allowed;
}

/* ✅ Meeting form */
.form-box {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.form-box input,
.form-box textarea {
  width: 250px;
  padding: 8px;
}

.form-box textarea {
  resize: none;
  height: 60px;
}

button {
  padding: 10px 20px;
}
</style>