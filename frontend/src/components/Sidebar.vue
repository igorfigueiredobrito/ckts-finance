<template>
  <aside class="sidebar">
    <!-- Removido o cabeçalho antigo pois foi pra Navbar -->
    <div class="sidebar-header">
      <span class="sidebar-title">Menu Principal</span>
    </div>

    <nav class="sidebar-nav">
      <router-link to="/" class="nav-item" exact-active-class="active">
        <LayoutDashboardIcon size="20" />
        <span>Dashboard</span>
      </router-link>
      <router-link to="/transacoes" class="nav-item" active-class="active">
        <ReceiptIcon size="20" />
        <span>Transações</span>
      </router-link>
      <router-link to="/categorias" class="nav-item" active-class="active">
        <TagsIcon size="20" />
        <span>Categorias</span>
      </router-link>
      <router-link to="/graficos" class="nav-item" active-class="active">
        <PieChartIcon size="20" />
        <span>Gráficos</span>
      </router-link>
      <router-link to="/data" class="nav-item" active-class="active">
        <DownloadCloudIcon size="20" />
        <span>Importar/Exportar</span>
      </router-link>
      <router-link to="/perfil" class="nav-item" active-class="active">
        <UserIcon size="20" />
        <span>Meu Perfil</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <button @click="logout" class="nav-item logout-btn">
        <LogOutIcon size="20" />
        <span>Encerrar Sessão</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { 
  LayoutDashboardIcon, 
  ReceiptIcon, 
  LogOutIcon,
  PieChartIcon,
  FileTextIcon,
  DownloadCloudIcon,
  UserIcon,
  TagsIcon
} from 'lucide-vue-next';

const router = useRouter();

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  router.push('/login');
};
</script>

<style scoped>
.sidebar {
  width: 250px;
  height: calc(100vh - var(--navbar-height) - 4rem);
  position: sticky;
  top: calc(var(--navbar-height) + 2rem);
  display: flex;
  flex-direction: column;
  background: transparent;
}

.sidebar-header {
  margin-bottom: 1.5rem;
  padding-left: 1rem;
}

.sidebar-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: var(--text-muted);
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s;
  font-weight: 500;
  font-size: 0.95rem;
  background: transparent;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  color: var(--text-main);
  background: var(--bg-card);
  box-shadow: var(--shadow-sm);
}

.nav-item.active {
  background: var(--primary-light);
  color: var(--primary);
  border-left-color: var(--primary);
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

.logout-btn {
  border-left: 3px solid transparent;
}

.logout-btn:hover {
  background: var(--danger-light);
  color: var(--danger);
}
</style>
