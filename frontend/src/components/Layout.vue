<script setup>
import { RouterView } from 'vue-router';
import Navbar from './Navbar.vue';
import Sidebar from './Sidebar.vue';
import Breadcrumb from './Breadcrumb.vue';
</script>

<template>
  <div class="app-layout">
    <Navbar />
    <div class="layout-body">
      <Sidebar />
      <main class="main-content">
        <!-- O RouterView injeta dinamicamente o Dashboard ou Transações -->
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.layout-body {
  display: flex;
  flex: 1;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
  padding: 2rem;
  gap: 2rem;
}

.main-content {
  flex: 1;
  min-width: 0;
}

@media (max-width: 768px) {
  .layout-body {
    flex-direction: column;
    padding: 1rem;
  }
}
</style>
