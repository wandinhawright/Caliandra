<template>
  <!-- Cart View - Design idêntico ao Django template ver_pedido.html -->
  <div class="cart-container">
    <div class="container">
      <!-- Cart with items -->
      <template v-if="!cartStore.isEmpty || cartStore.loading">
        <!-- Cart Header -->
        <div class="cart-header">
          <h2>
            <i class="fas fa-shopping-cart cart-icon"></i>
            Meu Carrinho
            <small class="ms-3" style="font-size: 1rem; opacity: 0.9;">
              {{ cartStore.totalItems }} 
              {{ cartStore.totalItems === 1 ? 'item' : 'itens' }}
            </small>
          </h2>
        </div>

        <!-- Loading state -->
        <div v-if="cartStore.loading && cartStore.items.length === 0" class="cart-body">
          <div class="text-center py-5">
            <div class="spinner-border text-warning" role="status">
              <span class="visually-hidden">Carregando...</span>
            </div>
            <p class="mt-3">Carregando carrinho...</p>
          </div>
        </div>

        <!-- Cart Body -->
        <div v-else class="cart-body">
          <CartItem
            v-for="item in cartStore.items"
            :key="item.id"
            :item="item"
            @removed="handleItemRemoved"
          />
        </div>

        <!-- Cart Total -->
        <div v-if="!cartStore.isEmpty" class="cart-summary text-end mt-4">
          <h4 style="font-family: 'Alexandria', sans-serif; color: #333;">
            Total do Pedido:
          </h4>
          <span id="cart-total" class="cart-total fs-3 fw-bold">
            {{ cartStore.formatCurrency(cartStore.totalPrice) }}
          </span>
        </div>

        <!-- Cart Actions -->
        <div v-if="!cartStore.isEmpty" class="cart-actions">
          <div class="action-left">
            <router-link to="/catalogo" class="btn btn-continue-shopping">
              <i class="fas fa-arrow-left"></i>
              Continuar Comprando
            </router-link>
          </div>
          
          <div class="action-right">
            <button 
              type="button" 
              class="btn btn-clear-cart"
              @click="handleClearCart"
              :disabled="cartStore.loading"
            >
              <i class="fas fa-trash"></i>
              Esvaziar Carrinho
            </button>
            <button 
              type="button" 
              class="btn btn-finalize" 
              id="btn-finalize-order"
              @click="handleFinalizeOrder"
              :disabled="cartStore.loading"
            >
              <i class="fas fa-check-circle"></i>
              Finalizar Pedido
            </button>
          </div>
        </div>
      </template>

      <!-- Empty Cart -->
      <template v-else>
        <div class="cart-header">
          <h2>
            <i class="fas fa-shopping-cart cart-icon"></i>
            Meu Carrinho
          </h2>
        </div>
        <div class="cart-body">
          <div class="empty-cart">
            <div class="empty-cart-icon">
              <i class="fas fa-shopping-cart"></i>
            </div>
            <h3>Seu carrinho está vazio</h3>
            <p>Que tal adicionar alguns de nossos produtos naturais ao seu carrinho?</p>
            <router-link to="/catalogo" class="btn btn-primary btn-lg mt-3">
              <i class="fas fa-leaf me-2"></i>
              Explorar Produtos
            </router-link>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCartStore } from '../stores/cart'
import CartItem from '../components/CartItem.vue'

const cartStore = useCartStore()

onMounted(() => {
  cartStore.fetchCart()
})

function handleItemRemoved(itemId) {
  console.log('Item removed:', itemId)
}

async function handleClearCart() {
  if (!confirm('Tem certeza que deseja esvaziar o carrinho?')) {
    return
  }
  
  try {
    await cartStore.clearCart()
  } catch (error) {
    alert('Erro ao esvaziar carrinho. Tente novamente.')
  }
}

async function handleFinalizeOrder() {
  const total = cartStore.formatCurrency(cartStore.totalPrice)
  
  const confirmed = confirm(
    `Tem certeza que deseja finalizar o pedido no valor de ${total}?\n\n` +
    `Após a confirmação, você receberá:\n` +
    `• Um e-mail com os detalhes do pedido\n` +
    `• Instruções de pagamento via WhatsApp\n` +
    `• Atualizações sobre a compra coletiva`
  )
  
  if (!confirmed) return
  
  try {
    await cartStore.finalizeOrder()
  } catch (error) {
    alert('Erro ao finalizar pedido. Tente novamente.')
  }
}
</script>

<style scoped>
/* Estilos já definidos em carrinho.css */

/* Estilos adicionais para os botões de ação */
.cart-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.action-left, .action-right {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-continue-shopping {
  background: #6c757d;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  font-weight: 600;
  transition: all 0.3s ease;
  font-family: 'Alexandria', sans-serif;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-continue-shopping:hover {
  background: #5a6268;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
  color: white;
  text-decoration: none;
}

@media (max-width: 768px) {
  .cart-actions {
    flex-direction: column;
  }
  
  .action-left, .action-right {
    width: 100%;
  }
  
  .cart-actions .btn {
    width: 100%;
  }
}
</style>
