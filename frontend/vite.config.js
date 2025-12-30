import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  
  build: {
    outDir: '../app/static/app/dist',
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html')
      }
    },
    assetsDir: 'assets',
    sourcemap: false
  },
  
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/atualizar-quantidade': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/remover-item': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/esvaziar-carrinho': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/finalizar-pedido': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  
  resolve: {
    alias: {
      '@': resolve(__dirname, './src')
    }
  }
})
