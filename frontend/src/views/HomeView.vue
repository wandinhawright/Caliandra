<template>
  <!-- Home View - Design baseado no início.html -->
  <div style="background: #fc9685">
    <div 
      class="bg-light border rounded border-light pt-5 pb-5 hero-travel jumbotron px-4" 
      data-aos="fade-up" 
      data-aos-once="true"
      style="background: url('/hero-bg.avif');"
    >
      <h1 class="hero-title" style="font-family: Alexandria, sans-serif;">
        Bem-Vindo(a) à Caliandra!
      </h1>
      <p class="hero-subtitle" style="color: rgb(0,0,0);font-family: Alexandria, sans-serif;">
        Aqui você pode participar de compras coletivas de produtos naturais de qualidade por preços acessíveis!
      </p>
      <p>
        <router-link 
          to="/catalogo"
          class="btn btn-primary btn-lg bg-success rounded-1 border-success hero-button" 
          type="button"
        >
          <small style="font-family:Alexandria, sans-serif;font-size:19px;color:black;">
            Saiba Mais
          </small>
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
// Home view matching Django template
</script>

<style scoped>
.hero-travel {
  min-height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background-size: cover !important;
  background-position: center !important;
  border-radius: 15px;
  margin: 2rem auto;
  max-width: 1200px;
}

.hero-title {
  font-size: 3rem;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  max-width: 800px;
}

.hero-button {
  padding: 1rem 2rem;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
  }
}
</style>
