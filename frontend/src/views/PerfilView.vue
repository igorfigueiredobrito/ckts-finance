<template>
  <div class="perfil-view animate-fade-in">
    <div class="page-header">
      <h1 class="font-serif">Meu Perfil</h1>
      <p class="text-muted">Gerencie suas informações pessoais e credenciais de segurança.</p>
    </div>

    <div class="perfil-container">
      
      <!-- Seção da Foto de Perfil -->
      <div class="glass-panel profile-photo-section">
        <h3>Foto de Perfil</h3>
        <p class="text-muted mb-4">Atualize sua foto para personalizar sua conta.</p>
        
        <div class="avatar-wrapper">
          <div class="avatar-container" @click="$refs.fileInput.click()">
            <img v-if="formData.foto_perfil" :src="`http://localhost:5001${formData.foto_perfil}`" alt="Perfil" class="avatar" />
            <div v-else class="avatar-placeholder">
              <CameraIcon size="32" class="text-muted" />
            </div>
            <div class="avatar-overlay">
              <UploadCloudIcon size="20" />
            </div>
          </div>
          <span class="upload-hint">Clique na imagem para alterar</span>
        </div>
        
        <input 
          type="file" 
          ref="fileInput" 
          style="display: none" 
          accept="image/*"
          @change="handleFotoUpload" 
        />
      </div>

      <!-- Coluna da Direita (Dados e Plano) -->
      <div class="profile-right-column">
        <!-- Seção de Dados Pessoais e Segurança -->
        <div class="glass-panel profile-data-section">
          <h3>Dados da Conta</h3>
          <p class="text-muted mb-4">Mantenha suas informações atualizadas.</p>
        
        <form @submit.prevent="salvarPerfil" class="perfil-form">
          <div class="form-row">
            <div class="form-group">
              <label>Nome Completo</label>
              <input type="text" v-model="formData.nome" class="form-control" required />
            </div>
            <div class="form-group">
              <label>E-mail</label>
              <input type="email" v-model="formData.email" class="form-control" required />
            </div>
          </div>

          <hr class="divider" />
          
          <h3>Segurança</h3>
          <p class="text-muted mb-4">Preencha apenas se desejar alterar sua senha.</p>

          <div class="form-row">
            <div class="form-group">
              <label>Senha Atual</label>
              <input type="password" v-model="formData.senha_atual" class="form-control" placeholder="••••••••" />
            </div>
            <div class="form-group">
              <label>Nova Senha</label>
              <input type="password" v-model="formData.nova_senha" class="form-control" placeholder="••••••••" />
            </div>
          </div>

          <div v-if="mensagem" :class="['feedback-msg', erro ? 'error' : 'success']">
            {{ mensagem }}
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Salvando...' : 'Salvar Alterações' }}
            </button>
          </div>
        </form>
      </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api/axios';
import { CameraIcon, UploadCloudIcon } from 'lucide-vue-next';

const formData = ref({
  nome: '',
  email: '',
  foto_perfil: '',
  senha_atual: '',
  nova_senha: ''
});

const loading = ref(false);
const mensagem = ref('');
const erro = ref(false);

onMounted(() => {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  formData.value.nome = user.nome || '';
  formData.value.email = user.email || '';
  formData.value.foto_perfil = user.foto_perfil || '';
});

const handleFotoUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const uploadData = new FormData();
  uploadData.append('file', file);

  try {
    const res = await api.post('/usuarios/upload-foto', uploadData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    // Atualiza preview imediatamente, mas só consolida no banco ao salvar.
    // Ou podemos atualizar direto, mas para UX simplificada, atualiza no Vue
    formData.value.foto_perfil = res.data.url;
    mensagem.value = 'Foto carregada! Clique em Salvar para consolidar.';
    erro.value = false;
  } catch (err) {
    erro.value = true;
    mensagem.value = 'Erro ao enviar imagem.';
  }
};

const salvarPerfil = async () => {
  loading.value = true;
  mensagem.value = '';
  
  if (formData.value.nova_senha && !formData.value.senha_atual) {
    erro.value = true;
    mensagem.value = 'Para criar uma nova senha, informe a senha atual.';
    loading.value = false;
    return;
  }

  try {
    const payload = {
      nome: formData.value.nome,
      email: formData.value.email,
      foto_perfil: formData.value.foto_perfil
    };

    if (formData.value.nova_senha) {
      payload.senha_atual = formData.value.senha_atual;
      payload.nova_senha = formData.value.nova_senha;
    }

    const response = await api.put('/usuarios/perfil', payload);
    
    // Atualiza o local storage
    localStorage.setItem('user', JSON.stringify(response.data.usuario));
    
    erro.value = false;
    mensagem.value = response.data.mensagem;
    
    // Limpar campos de senha
    formData.value.senha_atual = '';
    formData.value.nova_senha = '';
    
    // Dispara evento manual pra atualizar a navbar
    window.dispatchEvent(new Event('storage'));

  } catch (err) {
    erro.value = true;
    mensagem.value = err.response?.data?.mensagem || 'Erro ao atualizar perfil.';
  } finally {
    loading.value = false;
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

.perfil-container {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}

.profile-photo-section {
  width: 300px;
  padding: 2rem;
  text-align: center;
  flex-shrink: 0;
}

.avatar-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.avatar-container {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  position: relative;
  cursor: pointer;
  overflow: hidden;
  border: 3px solid var(--border-darker);
  transition: all 0.2s;
  background: var(--bg-light);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-container:hover {
  border-color: var(--primary);
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0;
  transition: opacity 0.2s;
}

.avatar-container:hover .avatar-overlay {
  opacity: 1;
}

.upload-hint {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.profile-data-section {
  padding: 2rem;
}

.profile-data-section h3 {
  font-size: 1.25rem;
  color: var(--text-main);
  margin-bottom: 0.25rem;
}

.mb-4 {
  margin-bottom: 1.5rem;
}

.form-row {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  flex: 1;
}

.form-group label {
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-main);
  margin-bottom: 0.5rem;
}

.divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 2rem 0;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
}

.feedback-msg {
  margin-top: 1.5rem;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
}

.feedback-msg.success {
  background: var(--primary-light);
  color: var(--primary-hover);
}

.feedback-msg.error {
  background: var(--danger-light);
  color: var(--danger);
}

.profile-right-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

@media (max-width: 768px) {
  .perfil-container {
    flex-direction: column;
  }
  .profile-photo-section {
    width: 100%;
  }
  .form-row {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
