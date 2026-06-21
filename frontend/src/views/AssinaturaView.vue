<template>
  <div class="assinatura-container animate-fade-in">
    <div class="header">
      <h1 class="page-title">Minha Assinatura</h1>
      <p class="subtitle">Escolha o plano ideal para suas metas financeiras.</p>
    </div>

    <div v-if="loading" class="text-center py-4">
      <p>Carregando planos disponíveis...</p>
    </div>

    <div v-else-if="planos.length === 0" class="text-center py-4 glass-panel">
      <p>Nenhum plano cadastrado no momento.</p>
    </div>

    <div v-else class="plans-grid">
      <div v-for="plano in planos" :key="plano.id" class="plan-card glass-panel">
        <div class="plan-header">
          <h3>{{ plano.nome }}</h3>
          <h2 class="plan-price">R$ {{ parseFloat(plano.preco).toFixed(2) }}<span class="period">/mês</span></h2>
        </div>
        
        <div class="plan-body">
          <p>{{ plano.descricao }}</p>
        </div>
        
        <div class="plan-footer">
          <button v-if="planoAtualId === plano.id" disabled class="btn-assinar btn-current">
            Seu plano atual
          </button>
          <button v-else
            @click="assinarPlano(plano.id)" 
            class="btn-assinar"
            :disabled="actionLoading === plano.id"
          >
            <template v-if="actionLoading === plano.id">Processando...</template>
            <template v-else-if="planoAtual && parseFloat(plano.preco) > parseFloat(planoAtual.preco)">Fazer Upgrade</template>
            <template v-else-if="planoAtual && parseFloat(plano.preco) < parseFloat(planoAtual.preco)">Fazer Downgrade</template>
            <template v-else>Assinar Plano</template>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api/axios';

const planos = ref([]);
const loading = ref(true);
const actionLoading = ref(null);
const planoAtualId = ref(null);
const planoAtual = ref(null);

const fetchPlanos = async () => {
  loading.value = true;
  try {
    const [resPlanos, resMinhas] = await Promise.all([
      api.get('/planos'),
      api.get('/assinaturas/minhas')
    ]);
    planos.value = resPlanos.data;
    
    const ativa = resMinhas.data.find(a => a.status === 'ativo');
    if (ativa) {
      planoAtualId.value = ativa.id;
      // Precisamos comparar o ID da tabela planos, lembrando que na resposta de minhas assinaturas 
      // o a.id pode ser o ID do plano ou da relação. Vamos tentar associar direto com planos.value
      planoAtual.value = resPlanos.data.find(p => p.id === ativa.id) || null;
    }
  } catch (err) {
    console.error("Erro ao buscar planos:", err);
  } finally {
    loading.value = false;
  }
};

const assinarPlano = async (planoId) => {
  actionLoading.value = planoId;
  try {
    const response = await api.post('/assinaturas', { plano_id: planoId });
    alert(response.data.mensagem || 'Assinatura realizada com sucesso!');
    planoAtualId.value = planoId; // Atualiza o plano atual localmente
    planoAtual.value = planos.value.find(p => p.id === planoId) || null;
  } catch (err) {
    alert(err.response?.data?.mensagem || 'Erro ao realizar assinatura.');
  } finally {
    actionLoading.value = null;
  }
};

onMounted(() => {
  fetchPlanos();
});
</script>

<style scoped>
.assinatura-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.plan-card {
  display: flex;
  flex-direction: column;
  padding: 2rem;
  border-top: 4px solid var(--primary);
  transition: transform 0.2s, box-shadow 0.2s;
}

.plan-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
}

.plan-header {
  text-align: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.plan-header h3 {
  font-size: 1.25rem;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
}

.plan-price {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-main);
}

.period {
  font-size: 1rem;
  font-weight: 400;
  color: var(--text-muted);
}

.plan-body {
  flex-grow: 1;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.95rem;
  line-height: 1.5;
  margin-bottom: 2rem;
}

.btn-assinar {
  width: 100%;
  padding: 0.75rem;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-assinar:hover:not(:disabled) {
  background: var(--primary-dark);
}

.btn-assinar:disabled {
  background: var(--text-muted);
  cursor: not-allowed;
}

.text-center {
  text-align: center;
}

.py-4 {
  padding-top: 1.5rem;
  padding-bottom: 1.5rem;
}

.btn-current {
  background: var(--success-light);
  color: var(--success);
  border: 1px solid var(--success);
}
.btn-current:disabled {
  background: var(--success-light) !important;
  color: var(--success) !important;
  opacity: 0.8;
  cursor: default;
}
</style>
