<template>
  <div class="container">
    <div class="box">
      <h2>Book a Cabin</h2>

      <label>Date</label>
      <input type="date" v-model="date" />

      <label>From</label>
      <input type="time" v-model="fromTime" />

      <label>To</label>
      <input type="time" v-model="toTime" />

      <button @click="checkAvailability">Check Availability</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

const date = ref("")
const fromTime = ref("")
const toTime = ref("")

const checkAvailability = () => {
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