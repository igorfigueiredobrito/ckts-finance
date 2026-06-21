<template>
  <div class="cadastro-container">
    <div class="glass-panel cadastro-box animate-fade-in">
      <div class="cadastro-header">
        <h2 class="font-serif brand-title">Criar Conta</h2>
        <p class="subtitle">Cadastre-se para começar a controlar suas finanças.</p>
      </div>

      <form @submit.prevent="handleCadastro" class="cadastro-form">
        <div class="form-grid">
          <div class="form-group">
            <label>Nome Completo</label>
            <input type="text" v-model="form.nome" class="form-control" required placeholder="Seu nome" />
          </div>
          
          <div class="form-group">
            <label>E-mail</label>
            <input type="email" v-model="form.email" class="form-control" required placeholder="voce@email.com" />
          </div>
          
          <div class="form-group">
            <label>Senha</label>
            <input type="password" v-model="form.senha" class="form-control" required placeholder="••••••••" />
          </div>

          <div class="form-group">
            <label>CPF</label>
            <input type="text" v-model="form.cpf" class="form-control" placeholder="000.000.000-00" />
          </div>

          <div class="form-group">
            <label>Telefone</label>
            <input type="text" v-model="form.telefone" class="form-control" placeholder="(00) 00000-0000" />
          </div>

          <div class="form-group">
            <label>Data de Nascimento</label>
            <input type="date" v-model="form.data_nascimento" class="form-control" />
          </div>
        </div>

        <div v-if="erro" class="alert-error">
          {{ erro }}
        </div>
        
        <div v-if="sucesso" class="alert-success">
          Conta criada com sucesso! Redirecionando para login...
        </div>

        <div class="actions">
          <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
            {{ loading ? 'Processando...' : 'Pagar e Criar Conta' }}
          </button>
          <router-link to="/" class="btn btn-secondary btn-block mt-3" style="text-align: center;">Voltar</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '../api/axios';

const router = useRouter();
const route = useRoute();

const loading = ref(false);
const erro = ref('');
const sucesso = ref(false);

const form = reactive({
  nome: '',
  email: '',
  senha: '',
  cpf: '',
  telefone: '',
  data_nascimento: ''
});

onMounted(() => {
  // Inicializações futuras se necessário
});

const handleCadastro = async () => {
  loading.value = true;
  erro.value = '';
  sucesso.value = false;

  try {
    await api.post('/usuarios/registrar', {
      ...form,
      foto_perfil: null
    });
    
    sucesso.value = true;
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (err) {
    erro.value = err.response?.data?.mensagem || 'Erro ao criar conta.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.cadastro-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem 1rem;
  background: var(--bg-main);
}

.cadastro-box {
  width: 100%;
  max-width: 600px;
  padding: 3rem 2.5rem;
  border-radius: 20px;
}

.cadastro-header {
  text-align: center;
  margin-bottom: 2rem;
}

.brand-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: var(--text-muted);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-muted);
}

.actions {
  margin-top: 2rem;
}

.mt-3 {
  margin-top: 1rem;
}

.alert-error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.9rem;
  text-align: center;
  margin-bottom: 1rem;
}

.alert-success {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #10b981;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.9rem;
  text-align: center;
  margin-bottom: 1rem;
}
</style>
