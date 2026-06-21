<template>
  <div class="landing-page">
    <!-- Header / Navbar -->
    <header class="navbar glass-panel">
      <div class="nav-container">
        <div class="logo">
          <div class="logo-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M8 14V9a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v5"/>
              <path d="M12 2v20"/>
              <path d="M12 7h5a3 3 0 0 1 3 3v3a3 3 0 0 1-3 3h-5"/>
              <path d="M12 11H7a3 3 0 0 0-3 3v3a3 3 0 0 0 3 3h5"/>
            </svg>
          </div>
          <span class="brand-title">Caktus Finance</span>
        </div>
        <div class="nav-actions">
          <router-link to="/login" class="btn btn-secondary">Entrar</router-link>
          <a href="#planos" class="btn btn-primary">Começar Agora</a>
        </div>
      </div>
    </header>

    <!-- Hero Section / Apresentação -->
    <section class="hero">
      <div class="hero-content animate-fade-in">
        <h1 class="hero-title">Domine suas finanças de forma simples e segura.</h1>
        <p class="hero-subtitle">
          Caktus Finance é a plataforma completa para você gerenciar receitas, 
          despesas, analisar gráficos do seu patrimônio e muito mais. 
          Criado para quem quer crescer.
        </p>
        <a href="#planos" class="btn btn-primary btn-lg pulse-hover">Ver Planos</a>
      </div>
    </section>

    <!-- Planos Section -->
    <section id="planos" class="planos-section">
      <h2 class="section-title">Escolha o plano ideal para você</h2>
      <div class="planos-grid">
        
        <!-- Básico -->
        <div class="plano-card glass-panel">
          <h3 class="plano-nome">Básico</h3>
          <div class="plano-preco">Gratuito</div>
          <ul class="plano-features">
            <li>Lançamentos limitados a 100/mês</li>
            <li>Dashboard simples</li>
            <li>Suporte da comunidade</li>
          </ul>
          <button @click="escolherPlano('Básico')" class="btn btn-secondary btn-block">Selecionar Básico</button>
        </div>

        <!-- Pro -->
        <div class="plano-card glass-panel plano-destaque">
          <div class="badge">Mais Popular</div>
          <h3 class="plano-nome">Pro</h3>
          <div class="plano-preco">R$ 29,90<span>/mês</span></div>
          <ul class="plano-features">
            <li>Lançamentos ilimitados</li>
            <li>Dashboard avançado com filtros</li>
            <li>Suporte por email</li>
          </ul>
          <button @click="escolherPlano('Pro')" class="btn btn-primary btn-block">Assinar Pro</button>
        </div>

        <!-- Premium -->
        <div class="plano-card glass-panel">
          <h3 class="plano-nome">Premium</h3>
          <div class="plano-preco">R$ 49,90<span>/mês</span></div>
          <ul class="plano-features">
            <li>Tudo do plano Pro</li>
            <li>Importação/Exportação de dados</li>
            <li>Gerente de conta dedicado</li>
          </ul>
          <button @click="escolherPlano('Premium')" class="btn btn-secondary btn-block">Assinar Premium</button>
        </div>

      </div>
    </section>

    <footer class="footer">
      <p>&copy; 2026 Caktus Finance. Todos os direitos reservados.</p>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const escolherPlano = (plano) => {
  router.push({ name: 'Cadastro', query: { plano } });
};
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  background: var(--bg-main);
  color: var(--text-main);
  font-family: 'Inter', sans-serif;
  overflow-x: hidden;
}

/* Navbar */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: var(--navbar-height);
  z-index: 100;
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(10px);
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  padding: 0 2rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: var(--primary);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
}

.brand-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-dark);
  font-family: 'Outfit', sans-serif;
}

.nav-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

/* Hero */
.hero {
  padding: 10rem 2rem 6rem;
  text-align: center;
  background: radial-gradient(circle at center, rgba(16, 185, 129, 0.05) 0%, transparent 70%);
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  color: #111827;
  font-family: 'Outfit', sans-serif;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: #4b5563;
  margin-bottom: 3rem;
  line-height: 1.6;
}

.btn-lg {
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
  border-radius: 12px;
}

/* Planos */
.planos-section {
  padding: 5rem 2rem 8rem;
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 4rem;
  color: #111827;
}

.planos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  align-items: center;
}

.plano-card {
  padding: 3rem 2rem;
  text-align: center;
  border-radius: 20px;
  position: relative;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.plano-card:hover {
  transform: translateY(-10px);
  box-shadow: var(--shadow-lg);
}

.plano-destaque {
  border: 2px solid var(--primary);
  background: white;
  transform: scale(1.05);
  box-shadow: var(--shadow-md);
}

.plano-destaque:hover {
  transform: scale(1.05) translateY(-10px);
}

.badge {
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--primary);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.plano-nome {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.plano-preco {
  font-size: 3rem;
  font-weight: 800;
  color: #111827;
  margin-bottom: 2rem;
}

.plano-preco span {
  font-size: 1rem;
  font-weight: 500;
  color: #6b7280;
}

.plano-features {
  list-style: none;
  padding: 0;
  margin-bottom: 2.5rem;
  text-align: left;
}

.plano-features li {
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border);
  color: #4b5563;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.plano-features li::before {
  content: "✓";
  color: var(--primary);
  font-weight: bold;
}

/* Footer */
.footer {
  text-align: center;
  padding: 2rem;
  border-top: 1px solid var(--border);
  color: #9ca3af;
  font-size: 0.9rem;
}
</style>
