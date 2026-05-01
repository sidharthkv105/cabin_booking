<template>
  <div class="container">
    <div class="box">
      <h2>Book a Cabin</h2>

      <!-- DATE -->
      <label>Date</label>
      <input type="date" v-model="date" />
      <p v-if="!date" class="error">Date is required</p>

      <!-- FROM -->
      <label>From</label>
      <input type="time" v-model="fromTime" />
      <p v-if="!fromTime" class="error">Start time is required</p>

      <!-- TO -->
      <label>To</label>
      <input type="time" v-model="toTime" />
      <p v-if="!toTime" class="error">End time is required</p>

      <!-- TIME VALIDATION -->
      <p v-if="timeError" class="error">
        Start time must be before end time
      </p>

      <!-- BUTTON -->
      <button :disabled="isInvalid" @click="checkAvailability">
        Check Availability
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

const date = ref("")
const fromTime = ref("")
const toTime = ref("")

/* 🔥 Time validation */
const timeError = computed(() => {
  if (!fromTime.value || !toTime.value) return false
  return fromTime.value >= toTime.value
})

/* 🔥 Disable button */
const isInvalid = computed(() => {
  return (
    !date.value ||
    !fromTime.value ||
    !toTime.value ||
    timeError.value
  )
})

const checkAvailability = () => {
  if (isInvalid.value) return

  router.push({
    path: "/cabins",
    query: {
      date: date.value,
      from: fromTime.value,
      to: toTime.value
    }
  })
}
</script>

<style>
.container {
  display: flex;
  justify-content: center;
  margin-top: 50px;
}

.box {
  background: white;
  padding: 30px;
  border-radius: 10px;
  width: 500px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

input {
  padding: 8px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

button {
  margin-top: 10px;
  padding: 10px;
  border-radius: 6px;
  border: none;
  background: #4f46e5;
  color: white;
  cursor: pointer;
}

button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.error {
  color: red;
  font-size: 12px;
  margin-top: -5px;
}
</style>