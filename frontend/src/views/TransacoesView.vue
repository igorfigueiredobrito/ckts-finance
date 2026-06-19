<template>
  <div class="transacoes-container animate-fade-in">
    <!-- Header de Controles -->
    <div class="header-actions glass-panel">
      <div class="actions-left">
        <button class="btn btn-primary" style="margin-right: 0.5rem;" @click="openModal(null, 'receita')">
          <PlusIcon size="18"/> Adicionar Receita
        </button>
        <button class="btn btn-danger" @click="openModal(null, 'despesa')">
          <PlusIcon size="18"/> Registrar Despesa
        </button>
      </div>
      <div class="actions-right">
        <!-- Input escondido para Upload Multipart JSON -->
        <input type="file" ref="importInput" style="display: none" accept=".json" @change="handleImport" />
        
        <button class="btn btn-outline" @click="$refs.importInput.click()" title="Importar Lote de JSON">
          <UploadCloudIcon size="18"/> Importar Lote JSON
        </button>
        <button class="btn btn-outline" @click="handleExportJSON" title="Exportar tabela atual para JSON">
          <DownloadCloudIcon size="18"/> Exportar Dados JSON
        </button>
        <button class="btn btn-outline" @click="handleExportXML" title="Baixar histórico de ações no MongoDB em formato XML">
          <DatabaseIcon size="18"/> XML de Logs (Mongo)
        </button>
        <button class="btn btn-outline pdf-btn" @click="handleGeneratePDF" title="Gerar Relatório em PDF">
          <FileTextIcon size="18"/> Relatório PDF
        </button>
      </div>
    </div>
    
    <!-- Filtros de Pesquisa (Consumindo a Flask API dinamicamente) -->
    <div class="filters-panel glass-panel mb-4">
      <form @submit.prevent="applyFilters" class="filters-row">
        <div class="form-group flex-2">
          <label>Buscar por Descrição</label>
          <input type="text" v-model="filters.descricao" class="form-control" placeholder="Digite para buscar..." />
        </div>
        <div class="form-group flex-1">
          <label>Data Início</label>
          <input type="date" v-model="filters.start_date" class="form-control" />
        </div>
        <div class="form-group flex-1">
          <label>Data Fim</label>
          <input type="date" v-model="filters.end_date" class="form-control" />
        </div>
        <div class="filters-actions">
          <button type="submit" class="btn btn-primary">
            <SearchIcon size="18" /> Filtrar
          </button>
          <button type="button" class="btn btn-outline" @click="clearFilters">Limpar</button>
        </div>
      </form>
    </div>

    <!-- Feedback Global Não-intrusivo -->
    <div v-if="feedback.message" :class="['alert', feedback.type]">
      <span>{{ feedback.message }}</span>
      <button @click="feedback.message = ''" class="btn-icon">x</button>
    </div>

    <!-- Data Table Premium -->
    <div class="glass-panel table-wrapper">
      <table class="table">
        <thead>
          <tr>
            <th>Descrição</th>
            <th>Data</th>
            <th>Categoria</th>
            <th>Valor</th>
            <th class="text-right">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td colspan="5" class="text-center py-4">Carregando dados...</td></tr>
          <tr v-else-if="transacoes.length === 0"><td colspan="5" class="text-center py-4 text-muted">Nenhuma transação encontrada para estes filtros.</td></tr>
          
          <tr v-for="t in transacoes" :key="t.id" class="table-row">
            <td class="font-medium">{{ t.descricao }}</td>
            <td class="text-muted">{{ formatDate(t.data) }}</td>
            <td>
              <span :class="['badge', t.categoria_tipo === 'receita' ? 'badge-success' : 'badge-danger']">
                {{ t.categoria_nome || 'Desconhecida' }}
              </span>
            </td>
            <td :class="t.categoria_tipo === 'receita' ? 'text-success' : 'text-danger'">
              R$ {{ parseFloat(t.valor).toFixed(2) }}
            </td>
            <td class="actions-cell justify-end">
              <button class="btn-icon" @click="openModal(t, t.categoria_tipo)" title="Editar">
                <EditIcon size="18"/>
              </button>
              <button class="btn-icon btn-danger-text" @click="handleDelete(t.id)" title="Excluir Permanentemente">
                <TrashIcon size="18"/>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Form (Glassmorphism Modal) -->
    <div v-if="isModalOpen" class="modal-backdrop" @click.self="closeModal">
      <div class="glass-panel modal-content animate-fade-in">
        <h3 class="modal-title">
          {{ formData.id ? 'Editar ' : 'Nova ' }}
          {{ modalTipo === 'receita' ? 'Receita' : 'Despesa' }}
        </h3>
        
        <form @submit.prevent="handleSubmit" class="mt-4">
          <div class="form-group">
            <label>Descrição Curta</label>
            <input type="text" v-model="formData.descricao" class="form-control" required placeholder="Ex: Conta de Luz" />
          </div>
          
          <div class="form-row">
            <div class="form-group flex-1">
              <label>Valor (R$)</label>
              <input type="number" step="0.01" min="0.01" v-model="formData.valor" class="form-control" required placeholder="0.00" />
            </div>
            <div class="form-group flex-1">
              <label>Data de Competência</label>
              <input type="date" v-model="formData.data" class="form-control" required />
            </div>
          </div>
          
          <div class="form-group">
            <label>Categoria</label>
            <select v-model="formData.categoria_id" class="form-control" required>
              <option value="" disabled>Selecione uma categoria...</option>
              <option v-for="cat in categoriasFiltradas" :key="cat.id" :value="cat.id">
                {{ cat.nome }}
              </option>
            </select>
            <small v-if="categoriasFiltradas.length === 0" class="text-danger block mt-1">Nenhuma categoria encontrada para este tipo.</small>
          </div>
          
          <div v-if="formError" class="alert alert-error mb-4">
            {{ formError }}
          </div>

          <div class="modal-actions">
            <button type="button" class="btn btn-outline" @click="closeModal">Cancelar</button>
            <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
              {{ isSubmitting ? 'Salvando...' : 'Salvar Transação' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../api/axios';
import { PlusIcon, UploadCloudIcon, DownloadCloudIcon, DatabaseIcon, EditIcon, TrashIcon, FileTextIcon, SearchIcon } from 'lucide-vue-next';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

// --- State ---
const transacoes = ref([]);
const categorias = ref([]);
const loading = ref(true);
const isModalOpen = ref(false);
const isSubmitting = ref(false);
const formError = ref('');
const feedback = ref({ type: '', message: '' });

// modalTipo define se estamos adicionando/editando uma 'receita' ou 'despesa'
const modalTipo = ref('despesa'); 

const initialForm = { id: null, descricao: '', valor: '', data: '', categoria_id: '' };
const formData = ref({ ...initialForm });

// Objeto de Filtros reativo
const filters = ref({ descricao: '', start_date: '', end_date: '' });

// Computed Property para filtrar categorias no Dropdown
const categoriasFiltradas = computed(() => {
  return categorias.value.filter(cat => cat.tipo === modalTipo.value);
});

// --- Lifecycle & Fetch ---
const loadTransacoes = async () => {
  loading.value = true;
  try {
    const res = await api.get('/transacoes', { params: filters.value });
    transacoes.value = res.data;
  } catch (error) {
    showFeedback('error', 'Falha ao buscar transações filtradas da API.');
  } finally {
    loading.value = false;
  }
};

const loadCategorias = async () => {
  try {
    const res = await api.get('/categorias');
    categorias.value = res.data;
  } catch (error) {
    console.error('Falha ao buscar categorias', error);
  }
};

onMounted(() => {
  loadCategorias();
  loadTransacoes();
});

const applyFilters = () => { 
  loadTransacoes(); 
};

const clearFilters = () => {
  filters.value = { descricao: '', start_date: '', end_date: '' };
  loadTransacoes();
};

// --- Utilities ---
const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return new Date(d.getTime() + Math.abs(d.getTimezoneOffset()*60000)).toLocaleDateString('pt-BR');
};

const showFeedback = (type, message) => {
  feedback.value = { type, message };
  setTimeout(() => feedback.value.message = '', 6000); 
};

// --- CRUD Actions ---
const openModal = (t = null, tipo = 'despesa') => {
  formError.value = '';
  modalTipo.value = tipo;
  
  if (t) {
    const d = new Date(t.data);
    const dateFormatted = new Date(d.getTime() + Math.abs(d.getTimezoneOffset()*60000)).toISOString().split('T')[0];
    
    formData.value = { id: t.id, descricao: t.descricao, valor: t.valor, data: dateFormatted, categoria_id: t.categoria_id };
  } else {
    formData.value = { ...initialForm };
    // Pre-seleciona a data de hoje por padrão
    formData.value.data = new Date().toISOString().split('T')[0];
  }
  isModalOpen.value = true;
};

const closeModal = () => { isModalOpen.value = false; };

const handleSubmit = async () => {
  if (formData.value.valor <= 0) {
    formError.value = "O valor da transação deve ser estritamente maior que zero.";
    return;
  }
  if (!formData.value.descricao.trim()) {
    formError.value = "A descrição é obrigatória.";
    return;
  }
  if (!formData.value.categoria_id) {
    formError.value = "Por favor, selecione uma categoria.";
    return;
  }
  
  isSubmitting.value = true;
  try {
    const payload = {
      descricao: formData.value.descricao,
      valor: parseFloat(formData.value.valor),
      data: formData.value.data,
      categoria_id: parseInt(formData.value.categoria_id)
    };

    if (formData.value.id) {
      await api.put(`/transacoes/${formData.value.id}`, payload);
      showFeedback('success', '✨ Transação alterada com sucesso!');
    } else {
      await api.post('/transacoes', payload);
      showFeedback('success', '✨ Nova transação gravada no banco.');
    }
    closeModal();
    loadTransacoes();
  } catch (error) {
    formError.value = error.response?.data?.mensagem || "Ocorreu um erro no Servidor Flask.";
  } finally {
    isSubmitting.value = false;
  }
};

const handleDelete = async (id) => {
  if (!confirm("Você está prestes a excluir este registro permanentemente. Continuar?")) return;
  try {
    await api.delete(`/transacoes/${id}`);
    showFeedback('success', '🗑️ Registro apagado com sucesso.');
    loadTransacoes();
  } catch (error) {
    showFeedback('error', 'Falha ao deletar. Você tem permissão?');
  }
};

// --- Import / Export Actions ---
const handleExportJSON = async () => {
  try {
    const res = await api.get('/data/export/transacoes/json', { responseType: 'blob' });
    downloadBlob(res.data, 'transacoes.json');
  } catch (err) { showFeedback('error', 'Erro na exportação JSON.'); }
};

const handleExportXML = async () => {
  try {
    const res = await api.get('/data/export/logs/xml', { responseType: 'blob' });
    downloadBlob(res.data, 'auditoria_mongodb.xml');
  } catch (err) { showFeedback('error', 'Erro na exportação XML.'); }
};

const handleImport = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const fd = new FormData();
  fd.append('file', file);

  try {
    const res = await api.post('/data/import/transacoes/json', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
    showFeedback(res.data.falhas > 0 ? 'alert-error' : 'success', `Lote Concluído! ${res.data.importados} inseridas. ${res.data.falhas} falhas tratadas.`);
    loadTransacoes();
  } catch (err) {
    showFeedback('error', err.response?.data?.mensagem || 'Falha ao importar o arquivo.');
  }
  event.target.value = null;
};

// --- Geração de Relatório PDF (jsPDF) ---
const handleGeneratePDF = () => {
  if (transacoes.value.length === 0) {
    showFeedback('error', 'Aviso: Não há dados filtrados para gerar um relatório.');
    return;
  }

  const doc = new jsPDF('p', 'mm', 'a4');
  const userStr = localStorage.getItem('user');
  const user = userStr ? JSON.parse(userStr) : { nome: 'Desconhecido' };
  const dateNow = new Date().toLocaleString('pt-BR');

  doc.setFontSize(18);
  doc.setTextColor(40);
  doc.text('Relatório Financeiro de Transações', 14, 22);
  
  doc.setFontSize(10);
  doc.setTextColor(100);
  doc.text(`Solicitado por: ${user.nome}`, 14, 30);
  doc.text(`Data e Hora da Geração: ${dateNow}`, 14, 36);
  
  const filterStrings = [];
  if (filters.value.descricao) filterStrings.push(`Termo: "${filters.value.descricao}"`);
  if (filters.value.start_date) filterStrings.push(`De: ${formatDate(filters.value.start_date)}`);
  if (filters.value.end_date) filterStrings.push(`Até: ${formatDate(filters.value.end_date)}`);
  
  if (filterStrings.length > 0) {
    doc.text(`Filtros Aplicados: ${filterStrings.join(' | ')}`, 14, 42);
  } else {
    doc.text(`Filtros: Nenhum (Exibindo Histórico Geral)`, 14, 42);
  }

  const tableColumn = ["Descrição", "Data", "Categoria", "Tipo", "Valor (R$)"];
  const tableRows = [];
  let totalCalculado = 0;

  transacoes.value.forEach(t => {
    const valorNum = parseFloat(t.valor);
    if(t.categoria_tipo === 'receita') totalCalculado += valorNum;
    else if(t.categoria_tipo === 'despesa') totalCalculado -= valorNum;

    const rowData = [
      t.descricao,
      formatDate(t.data),
      t.categoria_nome || 'N/A',
      t.categoria_tipo.toUpperCase(),
      valorNum.toFixed(2)
    ];
    tableRows.push(rowData);
  });

  autoTable(doc, {
    head: [tableColumn],
    body: tableRows,
    startY: 50,
    theme: 'grid',
    styles: { fontSize: 9, cellPadding: 3, font: 'helvetica' },
    headStyles: { fillColor: [59, 130, 246] } 
  });

  const finalY = doc.lastAutoTable.finalY || 50;
  doc.setFontSize(12);
  doc.setFont('helvetica', 'bold');
  
  if (totalCalculado >= 0) doc.setTextColor(16, 185, 129); 
  else doc.setTextColor(239, 68, 68);
  
  doc.text(`Saldo Consolidado: R$ ${totalCalculado.toFixed(2)}`, 14, finalY + 10);
  doc.save('Relatorio_Financeiro.pdf');
};

const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(new Blob([blob]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};
</script>

<style scoped>
/* Estilos Base e Painel de Ações */
.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.actions-left {
  display: flex;
  gap: 1rem;
}

.actions-right {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.pdf-btn {
  border-color: var(--primary);
  color: var(--primary);
}

.pdf-btn:hover {
  background: var(--primary-light);
}

/* Painel de Filtros Avançado */
.filters-panel {
  padding: 1rem 1.5rem;
  margin-bottom: 1.5rem;
  border-left: 4px solid var(--primary);
}

.filters-row {
  display: flex;
  align-items: flex-end;
  gap: 1rem;
  flex-wrap: wrap;
}

.filters-actions {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.btn-outline {
  background: transparent;
  border: 1px solid var(--border-darker);
  color: var(--text-main);
}

.btn-outline:hover {
  background: var(--border);
  transform: translateY(-2px);
}

/* Tabela e Badges */
.table-wrapper { overflow-x: auto; }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 1.25rem 1.5rem; text-align: left; border-bottom: 1px solid var(--border); }
.table th { color: var(--text-muted); font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; }
.table-row:hover { background: var(--bg-light); }

.badge { padding: 0.35rem 0.85rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.03em; }
.badge-success { background: var(--primary-light); color: var(--primary-hover); }
.badge-danger { background: var(--danger-light); color: var(--danger); }

.text-success { color: var(--primary-hover); font-weight: 600;}
.text-danger { color: var(--danger); font-weight: 600;}
.text-center { text-align: center; }
.text-right { text-align: right; }
.justify-end { justify-content: flex-end; }
.font-medium { font-weight: 500; }
.block { display: block; }
.py-4 { padding-top: 1.5rem; padding-bottom: 1.5rem; }

.actions-cell { display: flex; gap: 0.5rem; }
.btn-danger-text { color: var(--danger); }

/* Modais e Forms */
.modal-backdrop { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(8px); display: flex; align-items: center; justify-content: center; z-index: 100; padding: 1rem; }
.modal-content { width: 100%; max-width: 550px; padding: 2.5rem; box-shadow: var(--shadow-lg); }
.modal-title { font-size: 1.25rem; font-weight: 600; }

.mt-1 { margin-top: 0.25rem; }
.mt-4 { margin-top: 1.5rem; }
.mb-4 { margin-bottom: 1.5rem; }

.form-group { margin-bottom: 1.5rem; }
.form-group label { display: block; margin-bottom: 0.5rem; font-size: 0.9rem; font-weight: 500; color: var(--text-muted); }

.form-row { display: flex; gap: 1rem; }
.flex-1 { flex: 1; }
.flex-2 { flex: 2; min-width: 200px; }

.modal-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border); }

/* Alerts de Feedback */
.alert { padding: 1rem 1.25rem; border-radius: 12px; margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center; font-weight: 500; }
.success { background: var(--primary-light); border: 1px solid var(--primary-light); color: var(--primary-hover); }
.error, .alert-error { background: var(--danger-light); border: 1px solid var(--danger-light); color: var(--danger); }
</style>
