<template>
  <div class="admin-container animate-fade-in">
    <div class="header">
      <h1 class="page-title">Painel Administrativo</h1>
      <p class="subtitle">Gestão global de usuários e assinaturas SaaS</p>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid" v-if="stats">
      <div class="stat-card glass-panel">
        <div class="stat-icon users-icon">
          <UsersIcon size="24" />
        </div>
        <div class="stat-content">
          <h3>Total de Usuários</h3>
          <p class="stat-value">{{ stats.total_usuarios }}</p>
        </div>
      </div>
      
      <div class="stat-card glass-panel">
        <div class="stat-icon active-icon">
          <ActivityIcon size="24" />
        </div>
        <div class="stat-content">
          <h3>Usuários Ativos</h3>
          <p class="stat-value">{{ stats.usuarios_ativos }}</p>
        </div>
      </div>

      <div class="stat-card glass-panel">
        <div class="stat-icon mrr-icon">
          <TrendingUpIcon size="24" />
        </div>
        <div class="stat-content">
          <h3>Receita Recorrente (MRR)</h3>
          <p class="stat-value text-primary">R$ {{ stats.mrr_estimado.toFixed(2) }}</p>
        </div>
      </div>

      <div class="stat-card glass-panel plans-card">
        <div class="stat-icon plans-icon">
          <AwardIcon size="24" />
        </div>
        <div class="stat-content plans-content">
          <h3>Distribuição de Planos</h3>
          <div class="plans-breakdown">
            <span class="plan-badge premium-badge" title="Premium">⭐ {{ stats.planos['Premium'] || 0 }}</span>
            <span class="plan-badge pro-badge" title="Pro">🚀 {{ stats.planos['Pro'] || 0 }}</span>
            <span class="plan-badge basic-badge" title="Básico">🌱 {{ stats.planos['Básico'] || 0 }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Users Table -->
    <div class="glass-panel mt-4">
      <div class="table-header">
        <h2>Gestão de Usuários</h2>
      </div>
      <div class="table-responsive">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>Email</th>
              <th>Plano</th>
              <th>Status</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="6" class="text-center py-4">Carregando usuários...</td>
            </tr>
            <tr v-else-if="usuarios.length === 0">
              <td colspan="6" class="text-center py-4">Nenhum usuário encontrado.</td>
            </tr>
            <tr v-else v-for="user in usuarios" :key="user.id">
              <td>#{{ user.id }}</td>
              <td>
                <div class="user-info">

                  <div>
                    <div class="user-name">{{ user.nome }}</div>
                    <div class="user-role" v-if="user.role === 'admin'">
                      <span class="badge-admin">Admin</span>
                    </div>
                  </div>
                </div>
              </td>
              <td>{{ user.email }}</td>
              <td>
                <span class="plano-badge">
                  {{ user.plano_escolhido || 'Nenhum' }}
                </span>
              </td>
              <td>
                <span class="status-badge" :class="user.status === 'ativo' ? 'status-active' : 'status-blocked'">
                  {{ user.status === 'ativo' ? 'Ativo' : 'Bloqueado' }}
                </span>
              </td>
              <td>
                <div class="actions-group" v-if="user.role !== 'admin'">
                  <button 
                    @click="alternarStatus(user.id)" 
                    class="btn-action"
                    :class="user.status === 'ativo' ? 'btn-danger' : 'btn-success'"
                    :disabled="actionLoading === user.id"
                  >
                    {{ actionLoading === user.id ? '...' : (user.status === 'ativo' ? 'Bloquear' : 'Desbloquear') }}
                  </button>
                  <button 
                    @click="deletarUsuario(user.id)" 
                    class="btn-action btn-danger"
                    :disabled="actionLoading === user.id"
                  >
                    Excluir
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Plans Table (Gerenciar Planos) -->
    <div class="glass-panel mt-4">
      <div class="table-header" style="display: flex; justify-content: space-between; align-items: center;">
        <h2>Gestão de Planos</h2>
        <button class="btn-action btn-success" @click="abrirModalPlano()">+ Novo Plano</button>
      </div>
      <div class="table-responsive">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>Preço</th>
              <th>Descrição</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="planosLoading">
              <td colspan="5" class="text-center py-4">Carregando planos...</td>
            </tr>
            <tr v-else-if="planos.length === 0">
              <td colspan="5" class="text-center py-4">Nenhum plano cadastrado.</td>
            </tr>
            <tr v-else v-for="plano in planos" :key="plano.id">
              <td>#{{ plano.id }}</td>
              <td><strong>{{ plano.nome }}</strong></td>
              <td>R$ {{ parseFloat(plano.preco).toFixed(2) }}</td>
              <td>{{ plano.descricao }}</td>
              <td>
                <div class="actions-group">
                  <button @click="deletarPlano(plano.id)" class="btn-action btn-danger" :disabled="planosActionLoading === plano.id">
                    Excluir
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Novo Plano -->
    <div v-if="mostrarModalPlano" class="modal-overlay">
      <div class="modal-content glass-panel">
        <h3>Adicionar Novo Plano</h3>
        <form @submit.prevent="salvarPlano" class="mt-4">
          <div class="form-group">
            <label>Nome do Plano</label>
            <input v-model="novoPlano.nome" type="text" class="form-control" required />
          </div>
          <div class="form-group">
            <label>Preço (R$)</label>
            <input v-model="novoPlano.preco" type="number" step="0.01" class="form-control" required />
          </div>
          <div class="form-group">
            <label>Descrição</label>
            <textarea v-model="novoPlano.descricao" class="form-control" rows="3" required></textarea>
          </div>
          <div class="actions-group mt-4" style="justify-content: flex-end;">
            <button type="button" class="btn-action" @click="mostrarModalPlano = false">Cancelar</button>
            <button type="submit" class="btn-action btn-success" :disabled="salvandoPlano">Salvar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { UsersIcon, ActivityIcon, TrendingUpIcon, AwardIcon } from 'lucide-vue-next';
import api from '../api/axios';

const stats = ref(null);
const usuarios = ref([]);
const loading = ref(true);
const actionLoading = ref(null);

const planos = ref([]);
const planosLoading = ref(true);
const planosActionLoading = ref(null);
const mostrarModalPlano = ref(false);
const salvandoPlano = ref(false);
const novoPlano = ref({ nome: '', preco: 0, descricao: '' });

const fetchData = async () => {
  loading.value = true;
  try {
    const [statsRes, usersRes] = await Promise.all([
      api.get('/admin/stats'),
      api.get('/admin/usuarios')
    ]);
    stats.value = statsRes.data;
    usuarios.value = usersRes.data;
  } catch (err) {
    console.error("Erro ao carregar dados admin:", err);
  } finally {
    loading.value = false;
  }
};

const alternarStatus = async (userId) => {
  actionLoading.value = userId;
  try {
    await api.patch(`/admin/usuarios/${userId}/status`);
    await fetchData();
  } catch (err) {
    alert(err.response?.data?.mensagem || 'Erro ao alterar status.');
  } finally {
    actionLoading.value = null;
  }
};

const deletarUsuario = async (userId) => {
  if (!confirm("Tem certeza que deseja excluir permanentemente este usuário?")) return;
  
  actionLoading.value = userId;
  try {
    await api.delete(`/admin/usuarios/${userId}`);
    await fetchData();
  } catch (err) {
    alert(err.response?.data?.mensagem || 'Erro ao excluir usuário.');
  } finally {
    actionLoading.value = null;
  }
};

const fetchPlanos = async () => {
  planosLoading.value = true;
  try {
    const res = await api.get('/planos');
    planos.value = res.data;
  } catch (err) {
    console.error("Erro ao buscar planos:", err);
  } finally {
    planosLoading.value = false;
  }
};

const abrirModalPlano = () => {
  novoPlano.value = { nome: '', preco: 0, descricao: '' };
  mostrarModalPlano.value = true;
};

const salvarPlano = async () => {
  salvandoPlano.value = true;
  try {
    await api.post('/planos', novoPlano.value);
    mostrarModalPlano.value = false;
    await fetchPlanos();
  } catch (err) {
    alert(err.response?.data?.mensagem || 'Erro ao criar plano.');
  } finally {
    salvandoPlano.value = false;
  }
};

const deletarPlano = async (id) => {
  if (!confirm("Tem certeza que deseja excluir este plano? Ele pode ter assinantes.")) return;
  planosActionLoading.value = id;
  try {
    await api.delete(`/planos/${id}`);
    await fetchPlanos();
  } catch (err) {
    alert(err.response?.data?.mensagem || 'Erro ao excluir plano.');
  } finally {
    planosActionLoading.value = null;
  }
};

onMounted(() => {
  fetchData();
  fetchPlanos();
});
</script>

<style scoped>
.admin-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.mt-4 {
  margin-top: 1.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.5rem;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.users-icon { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.active-icon { background: linear-gradient(135deg, #10b981, #059669); }
.mrr-icon { background: linear-gradient(135deg, #f59e0b, #d97706); }
.plans-icon { background: linear-gradient(135deg, #8b5cf6, #6d28d9); }

.stat-content h3 {
  font-size: 0.9rem;
  color: var(--text-muted);
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-main);
}

.text-primary {
  color: var(--primary);
}

/* Plan Breakdown specific styles */
.plans-content {
  width: 100%;
}
.plans-breakdown {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.25rem;
}
.plan-badge {
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 0.2rem;
}
.premium-badge {
  background: rgba(139, 92, 246, 0.15);
  color: #7c3aed;
  border: 1px solid rgba(139, 92, 246, 0.3);
}
.pro-badge {
  background: rgba(59, 130, 246, 0.15);
  color: #2563eb;
  border: 1px solid rgba(59, 130, 246, 0.3);
}
.basic-badge {
  background: rgba(16, 185, 129, 0.15);
  color: #059669;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.table-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.table-header h2 {
  font-size: 1.1rem;
  font-weight: 600;
}

.table-responsive {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  text-align: left;
  padding: 1rem 1.5rem;
  font-size: 0.85rem;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 600;
  border-bottom: 1px solid var(--border);
}

.data-table td {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--bg-body);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: var(--text-muted);
}

.user-name {
  font-weight: 500;
}

.badge-admin {
  font-size: 0.7rem;
  background: #3b82f6;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
}

.plano-badge {
  background: var(--bg-body);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.plan-select {
  padding: 0.4rem;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--bg-body);
  color: var(--text-main);
  font-size: 0.85rem;
  font-weight: 500;
}

.plan-select:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-active {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.status-blocked {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.actions-group {
  display: flex;
  gap: 0.5rem;
}

.btn-action {
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  border: none;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-action:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-success {
  background: var(--primary);
  color: white;
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.py-4 {
  padding-top: 1rem !important;
  padding-bottom: 1rem !important;
}

.text-center {
  text-align: center;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  width: 100%;
  max-width: 500px;
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.2rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-muted);
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--bg-body);
  color: var(--text-main);
  font-family: inherit;
  font-size: 0.95rem;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1);
}
</style>
