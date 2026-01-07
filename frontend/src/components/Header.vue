<template>
  <!-- Header com design idêntico ao Django template -->
  <div class="bg-success mt-0 pt-0 mb-0 pb-0">
    <header class="bg-primary bg-opacity-75 w-100 h-100" data-bs-theme="light">
      <div>
        <nav class="navbar navbar-expand-md bg-secondary ms-0 ps-0 pt-0 mb-0 pb-0" style="background: linear-gradient(#e7c1bb 0%, #F0D9D1 60%, #F4EFEC 99%)">
          <div class="container-fluid">
            <!-- Logo -->
            <router-link class="navbar-brand d-flex align-items-center" to="/">
            </router-link>
            <img 
              class="ms-0 mb-0 pb-0" 
              src="/logo.avif" 
              width="214" 
              height="146" 
              style="margin: -7px;" 
              alt="Caliandra Logo"
            >
            
            <!-- Toggle button for mobile -->
            <button 
              class="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navcol-3"
              aria-controls="navcol-3" 
              aria-expanded="false"
            >
              <span class="visually-hidden">Toggle navigation</span>
              <span class="navbar-toggler-icon"></span>
            </button>
            
            <!-- Navigation Menu -->
            <div class="collapse navbar-collapse ps-0 me-0 pe-0 mt-0 pt-0 pb-0" id="navcol-3">
              <ul class="navbar-nav mx-auto" style="font-size:20px;font-family:Amethysta, serif;">
                <li class="nav-item ms-0 me-3">
                  
                  <router-link 
                    class="nav-link me-3" 
                    to="/blog" 
                    style="color:var(--bs-black);"
                  >
                    Início
                  </router-link>
                </li>
                <li class="nav-item me-5 me-md-4 pe-md-0">
                  <router-link 
                    class="nav-link me-6 me-md-1" 
                    to="/catalogo" 
                    style="color: var(--bs-black);font-family: Amethysta, serif;"
                  >
                    Catálogo
                  </router-link>
                </li>
                <li class="nav-item me-5 md-0">
                  <a 
                    class="nav-link me-6 me-md-0" 
                    href="/contatos" 
                    style="color: var(--bs-black);font-family: Amethysta, serif;"
                  >
                    Contato
                  </a>
                </li>
                
                <!-- User section -->
                <li class="nav-item ms-5" v-if="!isAuthenticated">
                  <a 
                    class="btn btn-success rounded-pill border-2 ms-md-0 me-0" 
                    role="button" 
                    style="font-family:Amethysta, serif;background:#fc9685;border-color:#fc9685;" 
                    href="/login"
                  >
                    <i class="far fa-user" style="font-size:16px;color:black;"></i>
                    <small class="ms-md-2" style="font-family: Alexandria, sans-serif;font-size: 16px;color:black;">
                      Login
                    </small>
                  </a>
                </li>
                
                <li class="nav-item ms-0" v-if="isAuthenticated">
                  <a 
                    class="btn btn-success rounded-pill border-2 ms-md-0 me-0" 
                    role="button" 
                    style="font-family:Amethysta, serif;background:#fbaa70;border-color:#fbaa70;" 
                    href="/perfil"
                  >
                    <i class="far fa-user" style="font-size:16px;"></i>
                    <small class="ms-md-2" style="font-family: Alexandria, sans-serif;font-size: 16px;">
                      {{ userName || 'Usuário' }}
                    </small>
                  </a>
                </li>
                
                <li class="nav-item ms-0" v-if="isAuthenticated">
                  <a 
                    class="nav-link" 
                    href="/logout" 
                    style="color: var(--bs-black); font-family: Alexandria, sans-serif; font-size: 16px;"
                  >
                    Sair
                  </a>
                </li>
                
                <!-- Spacer -->
                <li class="nav-item ms-md-5"></li>
                
                <!-- Cart Icon -->
                <li class="nav-item">
                  <router-link to="/carrinho">
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      width="1em" 
                      height="1em" 
                      fill="#141415" 
                      viewBox="0 0 16 16" 
                      class="bi bi-cart4 me-0 pe-0" 
                      style="font-size: 30px;margin: -1px;height: 38px;width: 33px;padding: -11px;position: relative;"
                    >
                      <path d="M0 2.5A.5.5 0 0 1 .5 2H2a.5.5 0 0 1 .485.379L2.89 4H14.5a.5.5 0 0 1 .485.621l-1.5 6A.5.5 0 0 1 13 11H4a.5.5 0 0 1-.485-.379L1.61 3H.5a.5.5 0 0 1-.5-.5M3.14 5l.5 2H5V5zM6 5v2h2V5zm3 0v2h2V5zm3 0v2h1.36l.5-2zm1.11 3H12v2h.61zM11 8H9v2h2zM8 8H6v2h2zM5 8H3.89l.5 2H5zm0 5a1 1 0 1 0 0 2 1 1 0 0 0 0-2m-2 1a2 2 0 1 1 4 0 2 2 0 0 1-4 0m9-1a1 1 0 1 0 0 2 1 1 0 0 0 0-2m-2 1a2 2 0 1 1 4 0 2 2 0 0 1-4 0"></path>
                    </svg>
                    <span v-if="cartStore.totalItems > 0" class="cart-badge">
                      {{ cartStore.totalItems }}
                    </span>
                  </router-link>
                </li>
              </ul>
            </div>
          </div>
        </nav>
      </div>
    </header>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCartStore } from '../stores/cart'

const cartStore = useCartStore()

// TODO: Integrar com auth real
const isAuthenticated = computed(() => false)
const userName = computed(() => '')
</script>

<style scoped>
.cart-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: #dc3545;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: bold;
}

.nav-link.router-link-active {
  font-weight: bold;
}
</style>
