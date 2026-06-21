<template>
  <nav class="top-navbar">
    <div class="navbar-left">
      <div class="logo-box">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M8 14V9a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v5"/>
          <path d="M12 2v20"/>
          <path d="M12 7h5a3 3 0 0 1 3 3v3a3 3 0 0 1-3 3h-5"/>
          <path d="M12 11H7a3 3 0 0 0-3 3v3a3 3 0 0 0 3 3h5"/>
        </svg>
      </div>
      <span class="font-serif brand-title">Caktus Finance</span>
    </div>

    <div class="navbar-center">
      <router-link to="/app" class="nav-link">Dashboard</router-link>
      <router-link to="/app/transacoes" class="nav-link">Transações</router-link>
      <router-link to="/app/graficos" class="nav-link">Gráficos</router-link>
      <router-link to="/app/data" class="nav-link">Importação/Exportação</router-link>
    </div>

    <div class="navbar-right">
      <router-link to="/app/perfil" class="user-dropdown" style="text-decoration: none;">
        <UserIcon size="18" class="text-muted" />
        <span class="user-name">{{ user.nome ? user.nome.split(' ')[0] : 'Perfil' }}</span>
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { UserIcon } from 'lucide-vue-next';

const user = ref({});

const loadUser = () => {
  const stored = localStorage.getItem('user');
  if (stored) {
    user.value = JSON.parse(stored);
  }
};

onMounted(() => {
  loadUser();
  window.addEventListener('storage', loadUser);
});
</script>

<style scoped>
.top-navbar {
  height: var(--navbar-height);
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  position: sticky;
  top: 0;
  z-index: 50;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-box {
  width: 32px;
  height: 32px;
  background: var(--primary);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.text-white {
  color: white;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.navbar-center {
  display: flex;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  color: var(--text-muted);
  font-size: 0.95rem;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover, .nav-link.router-link-active {
  color: var(--text-main);
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.75rem;
  border: 1px solid var(--border-darker);
  border-radius: 20px;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.status-dot {
  width: 8px;
  height: 8px;
  background: var(--primary);
  border-radius: 50%;
  box-shadow: 0 0 0 2px var(--primary-light);
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.75rem;
  border: 1px solid var(--border-darker);
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.2s;
}

.user-dropdown:hover {
  background: var(--bg-light);
}

.user-name {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-main);
}
</style>
