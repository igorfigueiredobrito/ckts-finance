<template>
  <div class="dashboard animate-fade-in">
    
    <div class="page-header">
      <h1 class="font-serif">Painel Administrativo</h1>
      <p class="text-muted">Visão geral da plataforma e atalhos de gerenciamento financeiro.</p>
    </div>

    <!-- Seção: Visão Geral -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-header">
          <span class="stat-title">Receita Total</span>
          <TrendingUpIcon class="stat-icon text-primary" size="20" />
        </div>
        <div class="stat-body">
          <h2 class="stat-value text-primary">R$ {{ formatCurrency(displayReceitas) }}</h2>
          <span class="stat-desc">Receita bruta acumulada</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-header">
          <span class="stat-title">Despesas Totais</span>
          <TrendingDownIcon class="stat-icon text-danger" size="20" />
        </div>
        <div class="stat-body">
          <h2 class="stat-value text-danger">R$ {{ formatCurrency(displayDespesas) }}</h2>
          <span class="stat-desc">Gastos e saídas</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-header">
          <span class="stat-title">Saldo Atual</span>
          <WalletIcon class="stat-icon text-text-main" size="20" />
        </div>
        <div class="stat-body">
          <h2 class="stat-value">R$ {{ formatCurrency(displaySaldo) }}</h2>
          <span class="stat-desc">Caixa disponível</span>
        </div>
      </div>
    </div>

    <!-- Seção Admin -->
    <div v-if="isAdmin" class="admin-stats-section mt-4 mb-4">
      <h3 class="section-title">Métricas da Plataforma (Admin)</h3>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-title">Total de Usuários</span>
            <UsersIcon class="stat-icon text-primary" size="20" />
          </div>
          <div class="stat-body">
            <h2 class="stat-value">{{ Math.floor(displayTotalUsuarios).toLocaleString('pt-BR') }}</h2>
            <span class="stat-desc">Cadastrados no sistema</span>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-title">Receita Recorrente (MRR)</span>
            <ActivityIcon class="stat-icon text-primary" size="20" />
          </div>
          <div class="stat-body">
            <h2 class="stat-value text-primary">R$ {{ formatCurrency(displayMrr) }}</h2>
            <span class="stat-desc">Estimativa mensal em assinaturas</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Seção: Módulos de Gerenciamento -->
    <div class="modules-section">
      <h3>Módulos de Gerenciamento</h3>
      
      <div class="modules-grid">
        <router-link to="/app/transacoes" class="module-card">
          <ReceiptIcon size="24" class="module-icon" />
          <div class="module-content">
            <h4>Transações</h4>
            <p>Gerenciar receitas, despesas e categorias.</p>
          </div>
        </router-link>

        <router-link to="/app/graficos" class="module-card">
          <PieChartIcon size="24" class="module-icon" />
          <div class="module-content">
            <h4>Análise e Gráficos</h4>
            <p>Visualizar evolução patrimonial anual.</p>
          </div>
        </router-link>

        <router-link to="/app/data" class="module-card">
          <DownloadCloudIcon size="24" class="module-icon" />
          <div class="module-content">
            <h4>Importar/Exportar</h4>
            <p>Gerar relatórios em formato JSON ou XML.</p>
          </div>
        </router-link>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api/axios';
import { 
  TrendingUpIcon, 
  TrendingDownIcon, 
  WalletIcon,
  ReceiptIcon,
  PieChartIcon,
  DownloadCloudIcon,
  UsersIcon,
  ActivityIcon
} from 'lucide-vue-next';

const totalReceitas = ref(0);
const totalDespesas = ref(0);
const isAdmin = ref(false);
const adminStats = ref({});

const displayReceitas = ref(0);
const displayDespesas = ref(0);
const displaySaldo = ref(0);
const displayTotalUsuarios = ref(0);
const displayMrr = ref(0);

const formatCurrency = (val) => {
  return val.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
};

const animateValue = (targetRef, targetValue, duration = 1200) => {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    
    // easeOutQuart para uma animação suave que desacelera no final
    const easeProgress = 1 - Math.pow(1 - progress, 4);
    
    targetRef.value = easeProgress * targetValue;
    
    if (progress < 1) {
      window.requestAnimationFrame(step);
    } else {
      targetRef.value = targetValue;
    }
  };
  window.requestAnimationFrame(step);
};

onMounted(async () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  if (user.role === 'admin') {
    isAdmin.value = true;
    try {
      const resStats = await api.get('/admin/stats');
      adminStats.value = resStats.data;
      
      // Anima os números de admin
      animateValue(displayTotalUsuarios, resStats.data.total_usuarios || 0);
      animateValue(displayMrr, resStats.data.mrr_estimado || 0);
    } catch (e) {
      console.error('Erro ao buscar métricas de admin', e);
    }
  }

  try {
    const response = await api.get('/transacoes');
    const transacoes = response.data;
    
    let tempReceitas = 0;
    let tempDespesas = 0;
    
    transacoes.forEach(t => {
      const valor = parseFloat(t.valor);
      if (t.categoria_tipo === 'receita') {
        tempReceitas += valor;
      } else if (t.categoria_tipo === 'despesa') {
        tempDespesas += valor;
      }
    });
    
    totalReceitas.value = tempReceitas;
    totalDespesas.value = tempDespesas;
    
    // Anima os números das transações
    animateValue(displayReceitas, tempReceitas);
    animateValue(displayDespesas, tempDespesas);
    animateValue(displaySaldo, tempReceitas - tempDespesas);

  } catch (error) {
    console.error("Erro ao processar dados do Dashboard", error);
  }
});
</script>

<style scoped>
.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  margin-bottom: 0.25rem;
  color: var(--text-main);
  letter-spacing: -0.5px;
}

.page-header p {
  font-size: 0.95rem;
  color: var(--text-muted);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-title {
  color: var(--text-muted);
  font-size: 0.9rem;
  font-weight: 500;
}

.stat-icon {
  opacity: 0.8;
}

.text-text-main {
  color: var(--text-main);
}

.stat-body {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-value {
  font-size: 1.85rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.stat-desc {
  font-size: 0.8rem;
  color: var(--text-light);
}

/* Modules Section */
.modules-section {
  margin-top: 2rem;
}

.modules-section h3 {
  font-size: 1.15rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
  color: var(--text-main);
}

.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.module-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  text-decoration: none;
  color: inherit;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
}

.module-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-light);
}

.module-icon {
  color: var(--text-main);
  padding: 0.4rem;
  background: var(--bg-light);
  border-radius: 8px;
  box-sizing: content-box;
}

.module-content h4 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: var(--text-main);
}

.module-content p {
  font-size: 0.85rem;
  color: var(--text-muted);
  line-height: 1.4;
}

.mt-4 {
  margin-top: 2rem;
}

.mb-4 {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.15rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
  color: var(--text-main);
}
</style>
