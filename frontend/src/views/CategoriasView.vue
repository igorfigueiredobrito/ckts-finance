<template>
  <div class="categorias-container animate-fade-in">
    <div class="page-header">
      <h1 class="font-serif">Categorias</h1>
      <p class="text-muted">Gerencie as categorias usadas para classificar suas receitas e despesas.</p>
    </div>

    <div class="header-actions glass-panel mb-4">
      <button class="btn btn-primary" @click="openModal()">
        <PlusIcon size="18"/> Nova Categoria
      </button>
    </div>

    <!-- Feedback Global -->
    <div v-if="feedback.message" :class="['alert', feedback.type]">
      <span>{{ feedback.message }}</span>
      <button @click="feedback.message = ''" class="btn-icon">x</button>
    </div>

    <!-- Data Table -->
    <div class="glass-panel table-wrapper">
      <table class="table">
        <thead>
          <tr>
            <th>Nome da Categoria</th>
            <th>Tipo de Fluxo</th>
            <th class="text-right">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td colspan="3" class="text-center py-4">Carregando categorias...</td></tr>
          <tr v-else-if="categorias.length === 0"><td colspan="3" class="text-center py-4 text-muted">Nenhuma categoria cadastrada.</td></tr>
          
          <tr v-for="cat in categorias" :key="cat.id" class="table-row">
            <td class="font-medium">{{ cat.nome }}</td>
            <td>
              <span :class="['badge', cat.tipo === 'receita' ? 'badge-success' : 'badge-danger']">
                {{ cat.tipo === 'receita' ? 'Receita' : 'Despesa' }}
              </span>
            </td>
            <td class="actions-cell justify-end">
              <button class="btn-icon" @click="openModal(cat)" title="Editar">
                <EditIcon size="18"/>
              </button>
              <button class="btn-icon btn-danger-text" @click="handleDelete(cat.id)" title="Excluir">
                <TrashIcon size="18"/>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Form -->
    <div v-if="isModalOpen" class="modal-backdrop" @click.self="closeModal">
      <div class="glass-panel modal-content animate-fade-in">
        <h3 class="modal-title">{{ formData.id ? 'Editar Categoria' : 'Nova Categoria' }}</h3>
        
        <form @submit.prevent="handleSubmit" class="mt-4">
          <div class="form-group">
            <label>Nome da Categoria</label>
            <input type="text" v-model="formData.nome" class="form-control" required placeholder="Ex: Alimentação" />
          </div>
          
          <div class="form-group">
            <label>Tipo de Fluxo</label>
            <select v-model="formData.tipo" class="form-control" required>
              <option value="despesa">Despesa</option>
              <option value="receita">Receita</option>
            </select>
          </div>
          
          <div v-if="formError" class="alert alert-error mb-4">
            {{ formError }}
          </div>

          <div class="modal-actions">
            <button type="button" class="btn btn-outline" @click="closeModal">Cancelar</button>
            <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
              {{ isSubmitting ? 'Salvando...' : 'Salvar Categoria' }}
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api/axios';
import { PlusIcon, EditIcon, TrashIcon } from 'lucide-vue-next';

const categorias = ref([]);
const loading = ref(true);
const isModalOpen = ref(false);
const isSubmitting = ref(false);
const formError = ref('');
const feedback = ref({ type: '', message: '' });

const initialForm = { id: null, nome: '', tipo: 'despesa' };
const formData = ref({ ...initialForm });

const loadCategorias = async () => {
  loading.value = true;
  try {
    const res = await api.get('/categorias');
    categorias.value = res.data;
  } catch (error) {
    showFeedback('error', 'Falha ao buscar categorias da API.');
  } finally {
    loading.value = false;
  }
};

onMounted(loadCategorias);

const showFeedback = (type, message) => {
  feedback.value = { type, message };
  setTimeout(() => feedback.value.message = '', 6000); 
};

const openModal = (cat = null) => {
  formError.value = '';
  if (cat) {
    formData.value = { ...cat };
  } else {
    formData.value = { ...initialForm };
  }
  isModalOpen.value = true;
};

const closeModal = () => { isModalOpen.value = false; };

const handleSubmit = async () => {
  if (!formData.value.nome.trim()) {
    formError.value = "O nome da categoria é obrigatório.";
    return;
  }
  
  isSubmitting.value = true;
  try {
    const payload = {
      nome: formData.value.nome,
      tipo: formData.value.tipo
    };

    if (formData.value.id) {
      await api.put(`/categorias/${formData.value.id}`, payload);
      showFeedback('success', 'Categoria atualizada com sucesso!');
    } else {
      await api.post('/categorias', payload);
      showFeedback('success', 'Nova categoria cadastrada.');
    }
    closeModal();
    loadCategorias();
  } catch (error) {
    formError.value = error.response?.data?.mensagem || "Ocorreu um erro no Servidor Flask.";
  } finally {
    isSubmitting.value = false;
  }
};

const handleDelete = async (id) => {
  if (!confirm("Excluir esta categoria?")) return;
  try {
    await api.delete(`/categorias/${id}`);
    showFeedback('success', 'Categoria apagada com sucesso.');
    loadCategorias();
  } catch (error) {
    // Trata erro de integridade referencial vindo do Backend
    showFeedback('error', error.response?.data?.mensagem || 'Falha ao excluir categoria.');
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

.header-actions {
  display: flex;
  padding: 1.25rem 1.5rem;
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
.modal-content { width: 100%; max-width: 500px; padding: 2.5rem; box-shadow: var(--shadow-lg); }
.modal-title { font-size: 1.25rem; font-weight: 600; }

.mt-4 { margin-top: 1.5rem; }
.mb-4 { margin-bottom: 1.5rem; }

.form-group { margin-bottom: 1.5rem; }
.form-group label { display: block; margin-bottom: 0.5rem; font-size: 0.9rem; font-weight: 500; color: var(--text-muted); }

.modal-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border); }

.btn-outline {
  background: transparent;
  border: 1px solid var(--border-darker);
  color: var(--text-main);
}
.btn-outline:hover {
  background: var(--border);
}

/* Alerts de Feedback */
.alert { padding: 1rem 1.25rem; border-radius: 12px; margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center; font-weight: 500; }
.success { background: var(--primary-light); border: 1px solid var(--primary-light); color: var(--primary-hover); }
.error, .alert-error { background: var(--danger-light); border: 1px solid var(--danger-light); color: var(--danger); }
</style>
