<template>
  <div class="container">
    <div class="box">
      <h2>{{ title }}</h2>

      <slot />

      <p class="link">
        <slot name="footer" />
      </p>

      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  error: String
})
</script>

<style>
.container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
}

.box {
  width: 300px;
  padding: 25px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);

  display: flex;
  flex-direction: column;
  gap: 12px;
}

h2 {
  text-align: center;
  margin-bottom: 10px;
}

input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

input:focus {
  outline: none;
  border-color: #888;
}

button {
  margin-top: 10px;
  padding: 8px;
  border: none;
  background: #333;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background: #555;
}

.link {
  text-align: center;
  font-size: 13px;
}

.link span {
  cursor: pointer;
  color: #333;
  text-decoration: underline;
}

.error {
  color: red;
  font-size: 13px;
  text-align: center;
}
</style>