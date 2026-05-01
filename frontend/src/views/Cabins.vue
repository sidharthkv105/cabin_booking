<template>
  <div class="container">
    <h2>Select Cabin</h2>

    <!-- CABINS -->
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

    <!-- FORM -->
    <div v-if="selected" class="form-box">
      <h3>Meeting Details</h3>

      <!-- Meeting Name -->
      <input
        v-model="meetingName"
        placeholder="Meeting name"
        maxlength="15"
      />
      <p class="char-count">
        {{ meetingName.length }}/15
      </p>
      <p v-if="meetingName.length === 0" class="error">
        Meeting name is required
      </p>
      <p v-else-if="meetingName.length > 15" class="error">
        Max 15 characters allowed
      </p>

      <!-- Description -->
      <textarea
        v-model="description"
        placeholder="Description (optional)"
        maxlength="30"
      ></textarea>
      <p class="char-count">
        {{ description.length }}/30
      </p>
      <p v-if="description.length > 30" class="error">
        Max 30 characters allowed
      </p>

      <!-- Button -->
      <button
        :disabled="isInvalid"
        @click="confirmBooking"
      >
        Confirm Booking ({{ selected.name }})
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
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

/* 🔥 Validation */
const isInvalid = computed(() => {
  return (
    !meetingName.value ||
    meetingName.value.length > 15 ||
    description.value.length > 30
  )
})

const confirmBooking = async () => {
  if (isInvalid.value) return

  await axios.post(
    "http://localhost:8000/booking",
    {
      cabin_id: selected.value.id,
      date,
      from_time: from,
      to_time: to,
      meeting_name: meetingName.value,
      description: description.value
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

/* grid */
.grid {
  display: grid;
  grid-template-columns: repeat(2, 140px);
  gap: 15px;
  justify-content: center;
  margin-top: 20px;
}

.cabin {
  padding: 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.available {
  background: #d1fae5;
}

.booked {
  background: #fecaca;
  cursor: not-allowed;
}

/* form */
.form-box {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

/* 🔥 Bigger input */
.form-box input {
  width: 320px;
  padding: 12px;
  font-size: 14px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

/* 🔥 Bigger textarea */
.form-box textarea {
  width: 320px;
  height: 100px;
  padding: 12px;
  font-size: 14px;
  border-radius: 6px;
  border: 1px solid #ccc;
  resize: none;
}

/* char count */
.char-count {
  font-size: 12px;
  color: #888;
  margin-top: -5px;
}

/* error */
.error {
  color: red;
  font-size: 12px;
  margin-top: -5px;
}

/* button */
button {
  padding: 10px 20px;
  margin-top: 10px;
  border-radius: 6px;
  border: none;
  background: #4f46e5;
  color: white;
  cursor: pointer;
}

/* disabled */
button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}
</style>