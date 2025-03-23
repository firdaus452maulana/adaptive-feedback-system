<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <RouterView />
</template>

<style>
@import 'bootstrap/dist/css/bootstrap.min.css';
@import '@fortawesome/fontawesome-free/css/all.min.css';

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #FCE7C8;
}

:root {
  --primary-color: #B1C29E;
  --secondary-color: #F0A04B;
  --background-color: #FCE7C8;
  --text-color: #333;
  --text-secondary: #666;
}

* {
  box-sizing: border-box;
}

.btn {
  font-weight: 500;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.btn-primary:hover {
  background-color: #9fb08c;
  border-color: #9fb08c;
}

.btn-success {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
}

.btn-success:hover {
  background-color: #e09039;
  border-color: #e09039;
}
</style>