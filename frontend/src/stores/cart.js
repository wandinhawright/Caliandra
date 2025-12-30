import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

// Configurar axios para CSRF token do Django
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

export const useCartStore = defineStore('cart', () => {
  // State
  const items = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const totalItems = computed(() => {
    return items.value.reduce((sum, item) => sum + item.quantidade, 0)
  })

  const totalPrice = computed(() => {
    return items.value.reduce((sum, item) => sum + (item.preco * item.quantidade), 0)
  })

  const isEmpty = computed(() => items.value.length === 0)

  // Actions
  async function fetchCart() {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/carrinho/')
      
      if (response.data.success) {
        items.value = response.data.items || []
      }
    } catch (err) {
      error.value = err.message
      console.error('Error fetching cart:', err)
    } finally {
      loading.value = false
    }
  }

  async function updateQuantity(itemId, action) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/atualizar-quantidade/', {
        item_id: itemId,
        action: action
      })
      
      if (response.data.success) {
        // Atualiza o item localmente
        const item = items.value.find(i => i.id === itemId)
        if (item) {
          item.quantidade = response.data.nova_quantidade
        }
      }
      
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Error updating quantity:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function removeItem(itemId) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/remover-item/', {
        item_id: itemId
      })
      
      if (response.data.success) {
        items.value = items.value.filter(i => i.id !== itemId)
      }
      
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Error removing item:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function clearCart() {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/esvaziar-carrinho/')
      
      if (response.data.success) {
        items.value = []
      }
      
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Error clearing cart:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function finalizeOrder() {
    loading.value = true
    error.value = null
    
    try {
      // Redirect to Django finalize endpoint
      window.location.href = '/finalizar-pedido/'
    } catch (err) {
      error.value = err.message
      console.error('Error finalizing order:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value)
  }

  return {
    // State
    items,
    loading,
    error,
    
    // Getters
    totalItems,
    totalPrice,
    isEmpty,
    
    // Actions
    fetchCart,
    updateQuantity,
    removeItem,
    clearCart,
    finalizeOrder,
    formatCurrency
  }
})
