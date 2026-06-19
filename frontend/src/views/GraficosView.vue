<template>
  <div class="graficos-view animate-fade-in">
    <div class="page-header">
      <h1 class="font-serif">Análise Patrimonial</h1>
      <p class="text-muted">Explore seus dados financeiros através de múltiplos filtros e visualizações avançadas.</p>
    </div>

    <!-- Barra de Filtros Avançados -->
    <div class="glass-panel filters-bar">
      
      <div class="filter-group">
        <label>Período</label>
        <div class="date-inputs">
          <input type="date" v-model="dataInicio" class="form-control form-date" />
          <span class="date-separator">até</span>
          <input type="date" v-model="dataFim" class="form-control form-date" />
        </div>
      </div>
      
      <div class="filter-group">
        <label>Tipo de Fluxo</label>
        <select v-model="filtroTipo" class="form-control form-select">
          <option value="todos">Receitas e Despesas</option>
          <option value="receita">Apenas Receitas</option>
          <option value="despesa">Apenas Despesas</option>
        </select>
      </div>

      <div class="filter-group">
        <label>Visão</label>
        <select v-model="filtroVisao" class="form-control form-select">
          <option value="geral">Geral (Barras Totais)</option>
          <option value="topico">Por Tópico (Linhas por Categoria)</option>
        </select>
      </div>

    </div>

    <!-- Container do Gráfico -->
    <div class="chart-container glass-panel">
      <h3 class="chart-title">
        Evolução {{ filtroVisao === 'geral' ? 'Macro (Geral)' : 'Micro (Por Tópicos)' }}
      </h3>
      <div class="chart-wrapper">
        <Line 
          v-if="filtroVisao === 'geral' && chartDataGeral.datasets.length > 0" 
          :data="chartDataGeral" 
          :options="chartOptions" 
        />
        <Line 
          v-else-if="filtroVisao === 'topico' && chartDataTopico.datasets.length > 0" 
          :data="chartDataTopico" 
          :options="chartOptions" 
        />
        <div v-else class="text-center py-4 text-muted">Aguardando dados para o período e filtros selecionados...</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import api from '../api/axios';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
} from 'chart.js';
import { Bar, Line } from 'vue-chartjs';

ChartJS.register(CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend);

// Dados e Estado
const todasTransacoes = ref([]);

// Filtros
const dataInicio = ref('');
const dataFim = ref('');
const filtroTipo = ref('todos');
const filtroVisao = ref('geral');

// Data dos Gráficos
const chartDataGeral = ref({ labels: [], datasets: [] });
const chartDataTopico = ref({ labels: [], datasets: [] });

// Paleta de Cores para as Linhas de Tópicos
const categoryColors = [
  '#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ec4899', 
  '#ef4444', '#14b8a6', '#f43f5e', '#84cc16', '#06b6d4',
  '#64748b', '#d946ef', '#f97316'
];

onMounted(async () => {
  try {
    const response = await api.get('/transacoes');
    todasTransacoes.value = response.data;
    
    // Setar a data padrão (Últimos 6 meses até hoje)
    const hoje = new Date();
    const seisMesesAtras = new Date();
    seisMesesAtras.setMonth(hoje.getMonth() - 5);
    
    dataFim.value = hoje.toISOString().split('T')[0];
    dataInicio.value = seisMesesAtras.toISOString().split('T')[0];
    
    processarGraficos();

  } catch (error) {
    console.error("Erro ao buscar dados", error);
  }
});

// Assiste mudanças nos filtros e reprocessa
watch([dataInicio, dataFim, filtroTipo, filtroVisao], () => {
  processarGraficos();
});

const formataMesAno = (dataString) => {
  if (!dataString) return 'desconhecido';
  const d = new Date(dataString);
  const dataCorrigida = new Date(d.getTime() + Math.abs(d.getTimezoneOffset()*60000));
  const meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
  const ano = dataCorrigida.getFullYear().toString().slice(-2);
  return `${meses[dataCorrigida.getMonth()]}-${ano}`;
};

const processarGraficos = () => {
  // 1. Filtrar transações por Data e Tipo
  let transacoesFiltradas = todasTransacoes.value.filter(t => {
    if (!t.data) return false;
    const dataTx = new Date(t.data);
    
    // Filtro de Data
    if (dataInicio.value && new Date(dataInicio.value) > dataTx) return false;
    if (dataFim.value && new Date(dataFim.value) < dataTx) return false;
    
    // Filtro de Tipo
    if (filtroTipo.value !== 'todos' && t.categoria_tipo !== filtroTipo.value) return false;
    
    return true;
  });

  // Ordenar cronologicamente
  transacoesFiltradas.sort((a, b) => new Date(a.data) - new Date(b.data));

  // Identificar os períodos únicos (Meses) existentes no dataset filtrado para ser o Eixo X
  const labelSet = new Set();
  transacoesFiltradas.forEach(t => labelSet.add(formataMesAno(t.data)));
  const rotulosX = Array.from(labelSet);

  if (filtroVisao.value === 'geral') {
    processarGeral(transacoesFiltradas, rotulosX);
  } else {
    processarTopicos(transacoesFiltradas, rotulosX);
  }
};

const processarGeral = (dados, rotulosX) => {
  // Inicializar agrupadores
  const receitasMes = {};
  const despesasMes = {};
  rotulosX.forEach(r => { receitasMes[r] = 0; despesasMes[r] = 0; });

  dados.forEach(t => {
    const rotulo = formataMesAno(t.data);
    const valor = parseFloat(t.valor);
    if (t.categoria_tipo === 'receita') receitasMes[rotulo] += valor;
    if (t.categoria_tipo === 'despesa') despesasMes[rotulo] += valor;
  });

  const datasets = [];
  if (filtroTipo.value === 'todos' || filtroTipo.value === 'receita') {
    datasets.push({
      label: 'Receita primária',
      borderColor: '#0f172a',
      backgroundColor: '#0f172a',
      pointBackgroundColor: '#0f172a',
      borderWidth: 3,
      fill: false,
      tension: 0,
      pointRadius: 2,
      data: rotulosX.map(r => receitasMes[r])
    });
  }
  if (filtroTipo.value === 'todos' || filtroTipo.value === 'despesa') {
    datasets.push({
      label: 'Despesa primária',
      borderColor: '#ea580c',
      backgroundColor: '#ea580c',
      pointBackgroundColor: '#ea580c',
      borderWidth: 3,
      fill: false,
      tension: 0,
      pointRadius: 2,
      data: rotulosX.map(r => despesasMes[r])
    });
  }

  chartDataGeral.value = {
    labels: rotulosX,
    datasets: datasets
  };
};

const processarTopicos = (dados, rotulosX) => {
  // Estrutura: { "Alimentação": { "Jan/2023": 500, "Fev/2023": 400, "Total": 900 } }
  const topicos = {};

  dados.forEach(t => {
    const rotuloData = formataMesAno(t.data);
    const topicoNome = t.categoria_nome || 'Sem Tópico';
    const valor = parseFloat(t.valor);

    if (!topicos[topicoNome]) {
      topicos[topicoNome] = { Total: 0 };
      rotulosX.forEach(r => topicos[topicoNome][r] = 0);
    }
    
    topicos[topicoNome][rotuloData] += valor;
    topicos[topicoNome].Total += valor;
  });

  const datasets = Object.keys(topicos).map((nome, index) => {
    const dadosPorMes = rotulosX.map(r => topicos[nome][r]);
    const cor = categoryColors[index % categoryColors.length];
    
    // Legenda exibe o nome do tópico e seu total do período
    const legendaCustomizada = `${nome} (Total: R$ ${topicos[nome].Total.toFixed(2)})`;

    return {
      label: legendaCustomizada,
      borderColor: cor,
      backgroundColor: cor,
      pointBackgroundColor: '#ffffff',
      pointBorderColor: cor,
      pointBorderWidth: 2,
      pointRadius: 4,
      pointHoverRadius: 6,
      borderWidth: 3,
      fill: false,
      tension: 0, // Curva reta (estilo Banco Central)
      data: dadosPorMes
    };
  });

  // Ordenar datasets pelo Total (maior gasto/receita primeiro)
  datasets.sort((a, b) => {
    const totalA = parseFloat(a.label.split('R$ ')[1].replace(')', ''));
    const totalB = parseFloat(b.label.split('R$ ')[1].replace(')', ''));
    return totalB - totalA;
  });

  chartDataTopico.value = {
    labels: rotulosX,
    datasets: datasets
  };
};

// Configurações Comuns de Exibição
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: true,
      text: 'Receitas e despesas primárias reais',
      font: { size: 18, weight: 'bold', family: 'Arial, sans-serif' },
      color: '#000000',
      padding: { top: 10, bottom: 20 }
    },
    legend: {
      position: 'bottom',
      labels: { color: '#000000', font: { family: 'Arial, sans-serif', size: 14, weight: 'bold' }, padding: 30 }
    },
    tooltip: {
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      titleColor: '#1e293b',
      bodyColor: '#1e293b',
      borderColor: 'rgba(0,0,0,0.1)',
      borderWidth: 1,
      padding: 12,
      cornerRadius: 8,
      titleFont: { size: 14, weight: 'bold' },
      bodyFont: { size: 13 }
    }
  },
  scales: {
    y: {
      ticks: { color: '#000000', font: { size: 14, weight: 'bold' } },
      grid: { color: 'rgba(0,0,0,0.15)' }
    },
    x: {
      ticks: { 
        color: '#000000', 
        font: { size: 14, weight: 'bold' },
        maxRotation: 90,
        minRotation: 90
      },
      grid: { display: false }
    }
  }
};
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

.filters-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  padding: 1.5rem 2rem;
  margin-bottom: 2rem;
  background: var(--bg-card);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 600;
  color: var(--text-muted);
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.date-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-date {
  max-width: 150px;
}

.date-separator {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.form-select {
  min-width: 220px;
  cursor: pointer;
}

.chart-container {
  padding: 2rem;
  background: var(--bg-card);
}

.chart-title {
  margin-bottom: 1.5rem;
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--text-main);
  border-bottom: 1px solid var(--border);
  padding-bottom: 1rem;
}

.chart-wrapper {
  position: relative;
  height: 500px;
  width: 100%;
}

@media (max-width: 768px) {
  .filters-bar {
    flex-direction: column;
    gap: 1.5rem;
  }
  .date-inputs {
    flex-direction: column;
    align-items: flex-start;
  }
  .form-date {
    max-width: 100%;
  }
}
</style>
