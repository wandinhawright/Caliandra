<template>
  <!-- Registro Page -->
  <div class="register-container"style="background: #fffdf5;">
    <div class="container">
      <div class="row mb-5">
        <div class="col-md-8 col-xl-6 text-center ps-md-7 pe-md-7 mt-md-7 mx-auto">
          <h2 style="font-family: Alexandria, sans-serif; color: rgb(0,0,0);">
            Registre-se
          </h2>
          <p style="font-family: Alexandria, sans-serif;">
            Faça seu registro na Caliandra para poder fazer pedidos!
          </p>
        </div>
      </div>
      
      <div class="row d-flex justify-content-center">
        <div class="col-md-6 col-xl-4">
          <div class="card mb-5">
            <div class="card-body d-flex flex-column align-items-center" style="background: #f0d9d1;">
              
              <div class="bs-icon-xl bs-icon-circle bs-icon-primary  my-4 bs-icon"style="background: #fc9685;">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" 
                     viewBox="0 0 16 16" class="bi bi-person">
                  <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6m2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0m4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4m-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664z"></path>
                </svg>
              </div>
              
              <form class="text-center w-100" @submit.prevent="handleRegister">
                <div v-if="error" class="alert alert-danger mb-3" role="alert">
                  {{ error }}
                </div>
                
                <div class="mb-3">
                  <input 
                    v-model="form.nome"
                    class="form-control" 
                    type="text" 
                    placeholder="Nome completo"
                    style="font-family: Alexandria, sans-serif;"
                    required
                  >
                </div>
                
                <div class="mb-3">
                  <input 
                    v-model="form.email"
                    class="form-control" 
                    type="email" 
                    placeholder="E-mail"
                    style="font-family: Alexandria, sans-serif;"
                    required
                  >
                </div>
                
                <div class="mb-3">
                  <input 
                    v-model="form.telefone"
                    class="form-control" 
                    type="tel" 
                    placeholder="Telefone"
                    style="font-family: Alexandria, sans-serif;"
                  >
                </div>
                
                <div class="mb-3">
                  <input 
                    v-model="form.password"
                    class="form-control" 
                    type="password" 
                    placeholder="Senha"
                    style="font-family: Alexandria, sans-serif;"
                    required
                  >
                </div>
                
                <div class="mb-3">
                  <input 
                    v-model="form.confirmar_password"
                    class="form-control" 
                    type="password" 
                    placeholder="Confirmar senha"
                    style="font-family: Alexandria, sans-serif;"
                    required
                  >
                </div>
                
                <div class="mb-3">
                  <button 
                    class="btn btn-primary  w-100 d-block"style="background: #fc9685;" 
                    type="submit"
                    :disabled="loading"
                  >
                    <span style="font-size: 22px; font-family: Alexandria, sans-serif;">
                      {{ loading ? 'Registrando...' : 'Registrar' }}
                    </span>
                  </button>
                </div>
                
                <p class="text-muted" style="font-family: Alexandria, sans-serif;">
                  Já possui uma conta?&nbsp;
                  <router-link to="/login">Faça login aqui!</router-link>
                </p>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const form = ref({
  nome: '',
  email: '',
  telefone: '',
  password: '',
  confirmar_password: ''
})

const error = ref('')
const loading = ref(false)

const handleRegister = async () => {
  if (form.value.password !== form.value.confirmar_password) {
    error.value = 'As senhas não coincidem'
    return
  }
  
  try {
    loading.value = true
    error.value = ''
    
    const response = await axios.post('/api/auth/registro/', form.value)
    
    if (response.data.success) {
      // Redirect to verification page
      router.push('/verificacao')
    } else {
      error.value = response.data.error || 'Erro ao criar conta'
    }
    
  } catch (err) {
    error.value = err.response?.data?.error || 'Erro ao registrar. Tente novamente.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  background: rgba(255,255,255,0);
  min-height: 100vh;
  padding: 2rem 0;
}

.bs-icon-xl {
  width: 5rem;
  height: 5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bs-icon-circle {
  border-radius: 50%;
}

.bs-icon svg {
  width: 3rem;
  height: 3rem;
}

a {
  color: var(--bs-success);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
