<template>
  <!-- Verification Page -->
  <div class="verification-container">
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card" style="border-radius: 15px;">
            <div class="card-header" style="background: var(--bs-secondary); border-radius: 15px 15px 0 0;">
              <h2 style="font-family: 'Alexandria', sans-serif; margin: 0;">
                Verificação de Duas Etapas
              </h2>
            </div>
            
            <div class="card-body">
              <p style="font-family: 'Alexandria', sans-serif;">
                Enviamos um código de 6 dígitos para o seu e-mail. Por favor, insira-o abaixo para continuar.
              </p>
              
              <div v-if="success" class="alert alert-success" role="alert">
                {{ success }}
              </div>
              
              <div v-if="error" class="alert alert-danger" role="alert">
                {{ error }}
              </div>
              
              <form @submit.prevent="handleVerification">
                <div class="mb-3">
                  <label class="form-label" style="font-family: 'Alexandria', sans-serif;">
                    Código de Verificação
                  </label>
                  <input 
                    v-model="verificationCode"
                    class="form-control" 
                    type="text" 
                    placeholder="000000"
                    maxlength="6"
                    pattern="[0-9]{6}"
                    style="font-family: 'Alexandria', sans-serif; font-size: 2rem; text-align: center; letter-spacing: 0.5rem;"
                    required
                  >
                  <small class="text-muted">Digite os 6 dígitos recebidos por e-mail</small>
                </div>
                
                <button 
                  type="submit" 
                  class="btn btn-primary w-100 mt-3"
                  style="background: linear-gradient(135deg, #fbaa70 0%, #ff9f40 100%); border: none; font-family: 'Alexandria', sans-serif;"
                  :disabled="loading"
                >
                  {{ loading ? 'Verificando...' : 'Verificar Código' }}
                </button>
                
                <div class="text-center mt-3">
                  <button 
                    type="button"
                    @click="resendCode"
                    class="btn btn-link"
                    style="font-family: 'Alexandria', sans-serif;"
                    :disabled="resendDisabled"
                  >
                    {{ resendDisabled ? `Reenviar código em ${resendTimer}s` : 'Reenviar código' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const verificationCode = ref('')
const success = ref('')
const error = ref('')
const loading = ref(false)
const resendDisabled = ref(false)
const resendTimer = ref(60)

let timerInterval = null

const handleVerification = async () => {
  if (verificationCode.value.length !== 6) {
    error.value = 'O código deve ter 6 dígitos'
    return
  }
  
  try {
    loading.value = true
    error.value = ''
    
    await axios.post('/api/auth/verificacao/', {
      code: verificationCode.value
    })
    
    success.value = 'Código verificado com sucesso!'
    
    // Redirect to home after success
    setTimeout(() => {
      router.push('/')
    }, 2000)
    
  } catch (err) {
    error.value = err.response?.data?.error || 'Código inválido ou expirado'
  } finally {
    loading.value = false
  }
}

const resendCode = async () => {
  try {
    resendDisabled.value = true
    resendTimer.value = 60
    
    await axios.post('/verificacao/reenviar/')
    success.value = 'Código reenviado com sucesso!'
    
    // Start countdown
    timerInterval = setInterval(() => {
      resendTimer.value--
      if (resendTimer.value <= 0) {
        clearInterval(timerInterval)
        resendDisabled.value = false
      }
    }, 1000)
    
  } catch (err) {
    error.value = 'Erro ao reenviar código'
    resendDisabled.value = false
  }
}

onMounted(() => {
  // Auto-focus input
  setTimeout(() => {
    const input = document.querySelector('input[type="text"]')
    if (input) input.focus()
  }, 100)
})

onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval)
  }
})
</script>

<style scoped>
.verification-container {
  background: #fffedf;
  min-height: 100vh;
  padding: 2rem 0;
}

input[type="text"] {
  font-weight: bold;
}

input[type="text"]:focus {
  border-color: #fbaa70;
  box-shadow: 0 0 0 0.2rem rgba(251, 170, 112, 0.25);
}
</style>
