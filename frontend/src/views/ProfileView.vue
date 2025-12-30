<template>
  <!-- Profile Page -->
  <div class="profile-container">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card" style="border-radius: 15px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);">
            <div class="card-body" style="background: #f4dbaa; border-radius: 15px;">
              
              <div class="text-center mb-4">
                <div class="bs-icon-xl bs-icon-circle bs-icon-primary bg-success d-inline-flex justify-content-center align-items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" 
                       viewBox="0 0 16 16" class="bi bi-person">
                    <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6m2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0m4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4m-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664z"></path>
                  </svg>
                </div>
                <h2 class="mt-3" style="font-family: 'Amethysta', serif; color: #000;">
                  Meu Perfil
                </h2>
              </div>
              
              <form @submit.prevent="handleUpdateProfile">
                <div v-if="success" class="alert alert-success mb-3" role="alert">
                  {{ success }}
                </div>
                
                <div v-if="error" class="alert alert-danger mb-3" role="alert">
                  {{ error }}
                </div>
                
                <div class="mb-3">
                  <label class="form-label" style="font-family: 'Alexandria', sans-serif;">Nome</label>
                  <input 
                    v-model="form.nome"
                    class="form-control" 
                    type="text" 
                    style="font-family: 'Alexandria', sans-serif;"
                    required
                  >
                </div>
                
                <div class="mb-3">
                  <label class="form-label" style="font-family: 'Alexandria', sans-serif;">E-mail</label>
                  <input 
                    v-model="form.email"
                    class="form-control" 
                    type="email" 
                    style="font-family: 'Alexandria', sans-serif;"
                    disabled
                  >
                  <small class="text-muted">O e-mail não pode ser alterado</small>
                </div>
                
                <div class="mb-3">
                  <label class="form-label" style="font-family: 'Alexandria', sans-serif;">Telefone</label>
                  <input 
                    v-model="form.telefone"
                    class="form-control" 
                    type="tel" 
                    style="font-family: 'Alexandria', sans-serif;"
                  >
                </div>
                
                <div class="mb-3">
                  <label class="form-label" style="font-family: 'Alexandria', sans-serif;">Endereço</label>
                  <textarea 
                    v-model="form.endereco"
                    class="form-control" 
                    rows="3"
                    style="font-family: 'Alexandria', sans-serif;"
                  ></textarea>
                </div>
                
                <div class="d-grid gap-2">
                  <button 
                    class="btn btn-success" 
                    type="submit"
                    style="background: linear-gradient(135deg, #fbaa70 0%, #ff9f40 100%); border: none; font-family: 'Alexandria', sans-serif;"
                    :disabled="loading"
                  >
                    {{ loading ? 'Salvando...' : 'Salvar Alterações' }}
                  </button>
                  
                  <router-link 
                    to="/pedidos" 
                    class="btn btn-outline-primary"
                    style="font-family: 'Alexandria', sans-serif;"
                  >
                    <i class="fas fa-shopping-bag me-2"></i>
                    Meus Pedidos
                  </router-link>
                  
                  <button 
                    @click="handleLogout"
                    class="btn btn-outline-danger"
                    type="button"
                    style="font-family: 'Alexandria', sans-serif;"
                  >
                    <i class="fas fa-sign-out-alt me-2"></i>
                    Sair
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const form = ref({
  nome: '',
  email: '',
  telefone: '',
  endereco: ''
})

const success = ref('')
const error = ref('')
const loading = ref(false)

const fetchProfile = async () => {
  try {
    const response = await axios.get('/api/perfil/')
    // Assuming the API returns user data
    if (response.data.usuario) {
      form.value = { ...response.data.usuario }
    }
  } catch (err) {
    console.error('Erro ao carregar perfil:', err)
    // Redirect to login if not authenticated
    if (err.response?.status === 401 || err.response?.status === 403) {
      router.push('/login')
    }
  }
}

const handleUpdateProfile = async () => {
  try {
    loading.value = true
    error.value = ''
    success.value = ''
    
    const response = await axios.post('/api/perfil/atualizar/', form.value)
    
    if (response.data.success) {
      success.value = 'Perfil atualizado com sucesso!'
    } else {
      error.value = response.data.error || 'Erro ao atualizar perfil'
    }
    
  } catch (err) {
    error.value = 'Erro ao atualizar perfil. Tente novamente.'
  } finally {
    loading.value = false
  }
}

const handleLogout = async () => {
  try {
    await axios.post('/api/auth/logout/')
    router.push('/login')
  } catch (err) {
    console.error('Erro ao fazer logout:', err)
    router.push('/login')
  }
}

onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
.profile-container {
  background: #fffedf;
  min-height: 100vh;
  padding: 2rem 0;
}

.bs-icon-xl {
  width: 5rem;
  height: 5rem;
}

.bs-icon-circle {
  border-radius: 50%;
}

.bs-icon svg {
  width: 3rem;
  height: 3rem;
}
</style>
