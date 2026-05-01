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

    <button v-if="selected" @click="confirmBooking">
      Confirm Booking ({{ selected.name }})
    </button>
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
  if (!cabin.booked) selected.value = cabin
}

const confirmBooking = async () => {
  await axios.post(
    "http://localhost:8000/booking",
    {
      cabin_id: selected.value.id,
      date,
      from_time: from,
      to_time: to
    },
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`  // ✅ JWT
      }
    }
  )

  localStorage.setItem("bookingSuccess", "Booking successful")
  router.push("/dashboard")
}
</script>

<style>
.grid { display:grid; grid-template-columns:repeat(2,120px); gap:10px; justify-content:center; }
.cabin { padding:20px; text-align:center; border-radius:6px; cursor:pointer; }
.available { background:#d1fae5; }
.booked { background:#fecaca; cursor:not-allowed; }
</style>