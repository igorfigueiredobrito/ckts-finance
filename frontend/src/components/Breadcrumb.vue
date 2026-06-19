<template>
  <div class="breadcrumb animate-fade-in">
    <span>Visão Geral</span>
    <span class="separator">/</span>
    <span class="current">{{ $route.meta.title || $route.name }}</span>
  </div>
</template>

<style scoped>
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  margin-bottom: 2rem;
  color: var(--text-muted);
}

.separator {
  opacity: 0.5;
}

.current {
  color: var(--text-main);
  font-weight: 500;
}
</style>
