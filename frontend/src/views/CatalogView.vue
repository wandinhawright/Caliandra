<template>
  <!-- Catálogo de Produtos -->
  <div class="catalog-container">
    <div class="container py-4">
      <div class="row">
        <div class="col-12 text-center mb-4">
          <h2 style="font-family: 'Alexandria', sans-serif; color: #000;">
            Catálogo de Produtos
          </h2>
          <p style="font-family: 'Alexandria', sans-serif;">
            Produtos naturais de qualidade para seu bem-estar
          </p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status">
          <span class="visually-hidden">Carregando...</span>
        </div>
      </div>

      <!-- Products Grid -->
      <div v-else class="row g-4">
        <div 
          v-for="produto in produtos" 
          :key="produto.id"
          class="col-md-6 col-lg-4"
        >
          <div class="card h-100 product-card">
            <img 
              v-if="produto.imagem"
              :src="produto.imagem" 
              :alt="produto.nome"
              class="card-img-top product-image"
            >
            <div v-else class="card-img-top bg-secondary d-flex align-items-center justify-content-center" style="height: 200px;">
              <i class="fas fa-image fa-3x text-white"></i>
            </div>
            
            <div class="card-body">
              <h5 class="card-title" style="font-family: 'Amethysta', serif;">
                {{ produto.nome }}
              </h5>
              <p class="card-text text-muted small">
                {{ produto.marca }} - {{ produto.tipo }}
              </p>
              <p class="card-text">
                {{ produto.descricao }}
              </p>
              <div class="d-flex justify-content-between align-items-center mt-3">
                <span class="h4 mb-0" style="color: #fc9685;">
                  {{ formatPrice(produto.valor) }}
                </span>
                <button 
                  @click="addToCart(produto.id)"
                  class="btn btn-success"
                  style="background: linear-gradient(135deg, #fbaa70 0%, #ff9f40 100%); border: none;"
                >
                  <i class="fas fa-cart-plus me-2"></i>
                  Adicionar
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!loading && produtos.length === 0" class="col-12 text-center py-5">
          <i class="fas fa-shopping-basket" style="font-size: 4rem; color: #fbaa70;"></i>
          <h3 class="mt-4" style="font-family: 'Alexandria', sans-serif;">
            Nenhum produto disponível
          </h3>
          <p class="mt-3">
            Em breve teremos novos produtos naturais disponíveis!
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useRouter } from 'vue-router'
import axios from 'axios'

const cartStore = useCartStore()
const router = useRouter()

const produtos = ref([])
const loading = ref(true)

const formatPrice = (value) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

const fetchProdutos = async () => {
  try {
    loading.value = true
    const response = await axios.get('/api/produtos/')
    produtos.value = response.data.produtos || []
  } catch (error) {
    console.error('Erro ao buscar produtos:', error)
    // TODO: Show error toast
  } finally {
    loading.value = false
  }
}

const addToCart = async (produtoId) => {
  try {
    await axios.post(`/adicionar-ao-pedido/${produtoId}/`)
    await cartStore.fetchCart()
    // TODO: Show success toast
    alert('Produto adicionado ao carrinho!')
  } catch (error) {
    console.error('Erro ao adicionar produto:', error)
    alert('Erro ao adicionar produto ao carrinho')
  }
}

onMounted(() => {
  fetchProdutos()
})
</script>

<style scoped>
.catalog-container {
  background: #fffedf;
  min-height: 80vh;
  padding: 2rem 0;
}

.product-card {
  border-radius: 15px;
  border: 1px solid #f0d9d1;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(251, 170, 112, 0.3);
}

.product-image {
  height: 200px;
  object-fit: cover;
  border-radius: 15px 15px 0 0;
}

.card-title {
  color: #000;
  font-weight: bold;
}

.btn-success:hover {
  opacity: 0.9;
  transform: scale(1.05);
}
</style>
