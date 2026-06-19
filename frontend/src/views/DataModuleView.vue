<template>
  <div class="data-view animate-fade-in">
    <div class="page-header">
      <h1 class="font-serif">Importação e Exportação</h1>
      <p class="text-muted">Gerencie seus dados em lote ou baixe relatórios analíticos de segurança do servidor.</p>
    </div>

    <div class="modules-grid">
      
      <!-- Exportar Dados do Usuário (JSON) -->
      <div class="module-card">
        <div class="module-header">
          <DownloadCloudIcon class="module-icon text-primary" size="24" />
          <h3>Exportar Transações</h3>
        </div>
        <p class="module-desc">Baixe todas as suas transações em um arquivo <code>.json</code> estruturado para fins de backup ou uso em outras ferramentas.</p>
        <button @click="downloadJson" class="btn btn-primary" :disabled="loadingJson">
          {{ loadingJson ? 'Processando...' : 'Baixar Arquivo JSON' }}
        </button>
      </div>

      <!-- Exportar Logs (XML) -->
      <div class="module-card">
        <div class="module-header">
          <FileTextIcon class="module-icon text-primary" size="24" />
          <h3>Logs do Sistema (Auditoria)</h3>
        </div>
        <p class="module-desc">Como administrador, gere a extração em lote dos logs armazenados no MongoDB em formato <code>.xml</code> estruturado.</p>
        <button @click="downloadXml" class="btn btn-primary" :disabled="loadingXml">
          {{ loadingXml ? 'Processando...' : 'Baixar Arquivo XML' }}
        </button>
      </div>

      <!-- Importar Dados (JSON) -->
      <div class="module-card import-card">
        <div class="module-header">
          <UploadCloudIcon class="module-icon text-primary" size="24" />
          <h3>Importação em Lote</h3>
        </div>
        <p class="module-desc">Faça upload de um arquivo <code>.json</code> previamente exportado para restaurar ou injetar transações em massa.</p>
        
        <div class="upload-area" @click="$refs.jsonInput.click()">
          <span v-if="!selectedFile">Clique para selecionar o arquivo</span>
          <span v-else class="text-primary font-bold">{{ selectedFile.name }}</span>
        </div>
        <input 
          type="file" 
          ref="jsonInput" 
          accept=".json" 
          style="display:none" 
          @change="handleFileSelect" 
        />
        
        <button @click="uploadJson" class="btn btn-primary" :disabled="!selectedFile || loadingUpload" style="margin-top: 1rem;">
          {{ loadingUpload ? 'Enviando...' : 'Iniciar Importação' }}
        </button>

        <div v-if="uploadFeedback" :class="['feedback-msg', uploadError ? 'error' : 'success']">
          {{ uploadFeedback }}
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '../api/axios';
import { DownloadCloudIcon, FileTextIcon, UploadCloudIcon } from 'lucide-vue-next';

const loadingJson = ref(false);
const loadingXml = ref(false);
const loadingUpload = ref(false);

const jsonInput = ref(null);
const selectedFile = ref(null);
const uploadFeedback = ref('');
const uploadError = ref(false);

// Exportar Transações JSON
const downloadJson = async () => {
  loadingJson.value = true;
  try {
    const res = await api.get('/data/export/transacoes/json', { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'minhas_transacoes.json');
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (err) {
    alert("Erro ao exportar JSON.");
  } finally {
    loadingJson.value = false;
  }
};

// Exportar Logs XML
const downloadXml = async () => {
  loadingXml.value = true;
  try {
    const res = await api.get('/data/export/logs/xml', { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'auditoria_logs.xml');
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (err) {
    alert("Erro ao exportar XML.");
  } finally {
    loadingXml.value = false;
  }
};

// Importar Transações JSON
const handleFileSelect = (e) => {
  if (e.target.files.length > 0) {
    selectedFile.value = e.target.files[0];
    uploadFeedback.value = '';
  }
};

const uploadJson = async () => {
  if (!selectedFile.value) return;
  
  loadingUpload.value = true;
  uploadFeedback.value = '';
  
  const formData = new FormData();
  formData.append('file', selectedFile.value);
  
  try {
    const res = await api.post('/data/import/transacoes/json', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    uploadError.value = false;
    uploadFeedback.value = res.data.mensagem || 'Dados importados com sucesso!';
    selectedFile.value = null; // Limpa o estado
  } catch (err) {
    uploadError.value = true;
    uploadFeedback.value = err.response?.data?.erro || 'Falha ao importar o arquivo.';
  } finally {
    loadingUpload.value = false;
  }
};
</script>

<style scoped>
.page-header {
  margin-bottom: 2.5rem;
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

.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
}

.module-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
}

.module-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.module-icon {
  background: var(--bg-light);
  padding: 0.5rem;
  border-radius: 8px;
  box-sizing: content-box;
}

.module-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
}

.module-desc {
  color: var(--text-muted);
  font-size: 0.95rem;
  line-height: 1.5;
  margin-bottom: 2rem;
  flex: 1;
}

.upload-area {
  border: 2px dashed var(--border-darker);
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  background: var(--bg-light);
  transition: all 0.2s;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.upload-area:hover {
  border-color: var(--primary);
  background: var(--primary-light);
}

.font-bold {
  font-weight: 600;
}

.feedback-msg {
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
  text-align: center;
}

.feedback-msg.success {
  background: var(--primary-light);
  color: var(--primary-hover);
}

.feedback-msg.error {
  background: var(--danger-light);
  color: var(--danger);
}
</style>
