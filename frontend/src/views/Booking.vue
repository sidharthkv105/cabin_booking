<template>
  <div class="page-wrapper">
    <button class="icon-btn" @click="goBack">
      < Go back
    </button>

    <div class="container">
      <div class="box">
        <h2>Book a Cabin</h2>

        <!-- INLINE FORM -->
        <div class="row">
          
          <div class="field">
            <label>Date</label>
            <input ref="dateRef" class="input" placeholder="Select date" />
            <p v-if="!date" class="error">Required</p>
          </div>

          <div class="field">
            <label>From</label>
            <input ref="fromRef" class="input" placeholder="Start time" />
            <p v-if="!fromTime" class="error">Required</p>
          </div>

          <div class="field">
            <label>To</label>
            <input ref="toRef" class="input" placeholder="End time" />
            <p v-if="!toTime" class="error">Required</p>
          </div>

        </div>

        <p v-if="timeError" class="error center">
          Start time must be before end time
        </p>

        <button :disabled="isInvalid" @click="checkAvailability">
          Check Availability
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"
import flatpickr from "flatpickr"
import "flatpickr/dist/flatpickr.min.css"

const router = useRouter()

const date = ref("")
const fromTime = ref("")
const toTime = ref("")

const dateRef = ref(null)
const fromRef = ref(null)
const toRef = ref(null)
const goBack = () => {
  router.push("/dashboard")
}

/* 🔥 Initialize flatpickr */
onMounted(() => {
  flatpickr(dateRef.value, {
    dateFormat: "Y-m-d",
    minDate: "today",
    onChange: (_, dateStr) => {
      date.value = dateStr
    }
  })

  flatpickr(fromRef.value, {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true,
    onChange: (_, timeStr) => {
      fromTime.value = timeStr

      // 🔥 restrict TO time
      if (toRef.value._flatpickr) {
        toRef.value._flatpickr.set("minTime", timeStr)
      }
    }
  })

  flatpickr(toRef.value, {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true,
    onChange: (_, timeStr) => {
      toTime.value = timeStr
    }
  })
})

/* 🔥 Validation */
const timeError = computed(() => {
  if (!fromTime.value || !toTime.value) return false
  return fromTime.value >= toTime.value
})

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
/* container */
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

/* card */
.box {
  background: white;
  padding: 30px;
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

/* row layout */
.row {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

/* field */
.field {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* input */
.input {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 14px;
}

/* button */
button {
  margin-top: 20px;
  padding: 10px;
  width: 100%;
  border-radius: 6px;
  border: none;
  background: #4f46e5;
  color: white;
  cursor: pointer;
  font-weight: 500;
}

button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

/* error */
.error {
  color: red;
  font-size: 12px;
  margin-top: 5px;
}

.center {
  text-align: center;
}
</style>