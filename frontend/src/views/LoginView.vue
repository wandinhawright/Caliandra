<template>
  <!-- Login Page -->
  <div class="login-container">
    <div class="container">
      <div class="row d-flex justify-content-center">
        <div class="col-md-10 col-xl-5">
          <div class="card mb-5" style="background: rgba(255,255,255,0); border-color: var(--bs-primary);">
            <div class="card-body d-flex w-100 flex-column align-items-center ms-7 ps-0 pe-0 mt-10 pt-0 pb-0" 
                 style="background: var(--bs-secondary); border-radius: 57px;">
              
              <h2 class="mt-5" style="font-family: Amethysta, serif; color: rgb(0,0,0);">
                Log in
              </h2>
              <p class="ms-0 me-0 mb-3" style="font-family: Amethysta, serif;">
                Faça login para poder fazer pedidos!
              </p>
              
              <div class=" my-4 bs-icon-xl bs-icon-circle bs-icon-primary bs-icon" 
                   style="background: #fc9685; border-color: var(--bs-success); color: var(--bs-primary);">
                <svg class="bi bi-person" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" 
                     fill="currentColor" viewBox="0 0 16 16">
                  <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6m2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0m4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4m-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664z"></path>
                </svg>
              </div>
              
              <form class="text-center" @submit.prevent="handleLogin">
                <div v-if="error" class="alert alert-danger w-75 ms-5 mb-3" role="alert">
                  {{ error }}
                </div>
                
                <div class="mb-3">
                  <input 
                    v-model="form.email"
                    class="form-control w-75 ms-5" 
                    type="email" 
                    placeholder="E-mail" 
                    style="font-family: Amethysta, serif; border-color: var(--bs-success);"
                    required
                  >
                </div>
                
                <div class="mb-3">
                  <input 
                    v-model="form.password"
                    class="form-control w-75 ms-5" 
                    type="password" 
                    placeholder="Senha" 
                    style="font-family: Amethysta, serif; border-color: var(--bs-success);"
                    required
                  >
                </div>
                
                <div class="mb-3">
                  <button 
                    class="btn btn-primary w-50"  
                    type="submit" 
                    style="background: #fc9685; border-color: var(--bs-success); border-radius: 36px;"
                    :disabled="loading"
                  >
                    <span style="font-size: 20px; font-family: Amethysta, serif;">
                      {{ loading ? 'Entrando...' : 'Entrar' }}
                    </span>
                  </button>
                </div>
                
                <p class="text-muted mb-5" style="font-family: Amethysta, serif;">
                  Ainda não possui um Login?&nbsp;
                  <router-link to="/registro">Registre-se Aqui!</router-link>
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
  email: '',
  password: ''
})

const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const response = await axios.post('/api/auth/login/', {
      email: form.value.email,
      password: form.value.password
    })
    
    if (response.data.success) {
      // Redirect to home
      router.push('/')
    } else {
      error.value = response.data.error || 'Erro ao fazer login'
    }
    
  } catch (err) {
    error.value = err.response?.data?.error || 'Credenciais inválidas'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  background: var(--bs-danger);
  min-height: 100vh;
  display: flex;
  align-items: center;
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
