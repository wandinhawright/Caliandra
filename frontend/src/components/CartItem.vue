<template>
  <!-- Cart Item - Design idêntico ao Django template -->
  <div class="cart-item" :data-item-id="item.id">
    <div class="row align-items-center">
      <!-- Product Image -->
      <div class="col-md-2 col-3">
        <img 
          v-if="item.produto?.imagem" 
          :src="item.produto.imagem" 
          :alt="item.produto?.nome" 
          class="product-image"
        >
        <div 
          v-else 
          class="product-image d-flex align-items-center justify-content-center bg-light"
        >
          <i class="fas fa-leaf text-muted" style="font-size: 2rem;"></i>
        </div>
      </div>

      <!-- Product Info -->
      <div class="col-md-4 col-9">
        <div class="product-info">
          <h5 class="product-name">{{ item.produto?.nome || 'Produto' }}</h5>
          <p class="product-price">{{ formatCurrency(item.preco) }}</p>
          <small v-if="item.produto?.marca" class="text-muted">
            {{ item.produto.marca }}
          </small>
        </div>
      </div>

      <!-- Quantity Controls -->
      <div class="col-md-3 col-6 mt-3 mt-md-0">
        <div class="quantity-controls">
          <button 
            type="button" 
            class="quantity-btn quantity-btn-minus"
            @click="decreaseQuantity"
            :disabled="item.quantidade <= 1 || loading"
          >
            <i class="fas fa-minus"></i>
          </button>
          
          <input 
            type="number" 
            class="quantity-input"
            :value="item.quantidade"
            @input="handleQuantityInput"
            min="1"
            max="99"
            :disabled="loading"
          >
          
          <button 
            type="button" 
            class="quantity-btn quantity-btn-plus"
            @click="increaseQuantity"
            :disabled="loading"
          >
            <i class="fas fa-plus"></i>
          </button>
        </div>
      </div>

      <!-- Item Total & Remove -->
      <div class="col-md-2 col-4 mt-3 mt-md-0 text-end">
        <div class="d-flex flex-column align-items-end gap-2">
          <strong class="item-total">
            {{ formatCurrency(item.preco * item.quantidade) }}
          </strong>
          <button 
            type="button" 
            class="remove-btn" 
            title="Remover item"
            @click="handleRemove"
            :disabled="loading"
          >
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCartStore } from '../stores/cart'

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['removed'])

const cartStore = useCartStore()
const loading = ref(false)

function formatCurrency(value) {
  return cartStore.formatCurrency(value)
}

async function increaseQuantity() {
  loading.value = true
  try {
    await cartStore.updateQuantity(props.item.id, 'plus')
  } catch (error) {
    console.error('Error increasing quantity:', error)
  } finally {
    loading.value = false
  }
}

async function decreaseQuantity() {
  if (props.item.quantidade <= 1) return
  
  loading.value = true
  try {
    await cartStore.updateQuantity(props.item.id, 'minus')
  } catch (error) {
    console.error('Error decreasing quantity:', error)
  } finally {
    loading.value = false
  }
}

let debounceTimeout = null
function handleQuantityInput(event) {
  const newValue = parseInt(event.target.value) || 1
  
  clearTimeout(debounceTimeout)
  debounceTimeout = setTimeout(async () => {
    if (newValue < 1) {
      event.target.value = 1
      return
    }
    
    const diff = newValue - props.item.quantidade
    
    loading.value = true
    try {
      for (let i = 0; i < Math.abs(diff); i++) {
        await cartStore.updateQuantity(props.item.id, diff > 0 ? 'plus' : 'minus')
      }
    } catch (error) {
      console.error('Error updating quantity:', error)
    } finally {
      loading.value = false
    }
  }, 500)
}

async function handleRemove() {
  if (!confirm(`Deseja remover "${props.item.produto?.nome}" do carrinho?`)) {
    return
  }
  
  loading.value = true
  try {
    await cartStore.removeItem(props.item.id)
    emit('removed', props.item.id)
  } catch (error) {
    console.error('Error removing item:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Estilos já definidos em carrinho.css */
</style>
