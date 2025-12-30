# Guia de Integração Vue.js - Caliandra

## 🎉 Migração Concluída!

O frontend Django foi migrado para Vue.js mantendo **exatamente** o design visual original!

## 📂 Estrutura Criada

```
frontend/
├── src/
│   ├── assets/
│   │   ├── css/
│   │   │   ├── main.css         # Variáveis CSS do Django
│   │   │   └── carrinho.css     # Estilos do carrinho
│   │   └── img/
│   │       ├── logo.avif
│   │       └── imagem-do-whatsapp...avif
│   ├── components/
│   │   ├── Header.vue           # Navbar (réplica exata do Django)
│   │   └── CartItem.vue         # Item do carrinho
│   ├── views/
│   │   ├── HomeView.vue         # Página inicial (hero section)
│   │   ├── CatalogView.vue      # Catálogo (placeholder)
│   │   └── CartView.vue         # Carrinho completo
│   ├── stores/
│   │   └── cart.js              # Pinia store para carrinho
│   ├── router/
│   │   └── index.js             # Vue Router
│   ├── App.vue                  # Componente raiz
│   └── main.js                  # Entry point
├── package.json
├── vite.config.js               # Build para Django
└── index.html
```

## 🎨 Design Preservado

### Cores Caliandra
- **Primary**: `#fc9685` (laranja suave)
- **Secondary**: `#f0d9d1` (bege rosado)
- **Orange**: `#fbaa70` (laranja médio)
- **Light Orange**: `#ff9f40` (laranja claro)
- **Background**: `#fffedf` (amarelo creme)

### Fontes
- **Body**: Alexandria, sans-serif
- **Headings**: Amethysta, serif
- **Decorative**: Aguafina Script, Aldrich, Bad Script

### Componentes Replicados
✅ Header com navbar gradient
✅ Logo 214x146px
✅ Cart com controles de quantidade
✅ Botões com gradientes
✅ Hero section com background

## 🚀 Como Usar

### Desenvolvimento

#### 1. Terminal 1 - Django Backend:
```bash
python manage.py runserver
```

#### 2. Terminal 2 - Vite Dev Server:
```bash
cd frontend
npm run dev
```

#### 3. Acesse:
- **Django Original**: http://localhost:8000/
- **Vue.js Dev**: http://localhost:5173/
- **Vue.js Integrado**: http://localhost:8000/app/

### Produção

#### 1. Build do Vue:
```bash
cd frontend
npm run build
```

#### 2. Colete arquivos estáticos (opcional):
```bash
python manage.py collectstatic --noinput
```

#### 3. Execute Django:
```bash
python manage.py runserver
```

#### 4. Acesse:
- http://localhost:8000/app/

## 🔌 Endpoints da API

### Criados para o Vue:
- `GET /api/carrinho/` - Dados do carrinho em JSON
- `POST /ajax/atualizar-quantidade/` - Atualizar quantidade
- `POST /ajax/remover-item/` - Remover item
- `POST /ajax/esvaziar-carrinho/` - Esvaziar carrinho

### Exemplos de Requisição:

```javascript
// Buscar carrinho
axios.get('/api/carrinho/')
  .then(response => {
    console.log(response.data.carrinho);
  });

// Atualizar quantidade
axios.post('/ajax/atualizar-quantidade/', {
  item_id: 123,
  quantidade: 5
});

// Remover item
axios.post('/ajax/remover-item/', {
  item_id: 123
});
```

## 📝 Rotas Vue

- `/` - Home (hero section)
- `/catalogo` - Catálogo (em desenvolvimento)
- `/carrinho` - Carrinho de compras

## 🔐 Autenticação

O Vue utiliza a sessão do Django automaticamente:
- CSRF token configurado no Axios
- Cookies de sessão compartilhados
- LoginRequiredMixin nas views da API

## 🛠️ Próximos Passos

### Para o Usuário Implementar:

1. **CatalogView.vue**
   - Implementar listagem de produtos
   - Adicionar filtros/busca
   - Botão "Adicionar ao Carrinho"

2. **Autenticação**
   - Login/Registro no Vue
   - Rotas protegidas
   - Perfil do usuário

3. **Finalização de Pedido**
   - Checkout flow
   - Formulário de endereço
   - Confirmação

4. **Produtos**
   - Página de detalhes
   - Imagens do produto
   - Descrição completa

## 🐛 Troubleshooting

### Erro: "CSRF token missing"
**Solução**: Certifique-se de que o Django está rodando e os cookies estão habilitados.

### Erro: "Module not found"
**Solução**: Execute `npm install` no diretório frontend.

### Erro: "Connection refused :8000"
**Solução**: Inicie o Django backend com `python manage.py runserver`.

### Estilos não carregam
**Solução**: Execute `npm run build` novamente e verifique os arquivos em `app/static/app/dist/`.

## 📊 Arquivos Modificados no Django

### `app/views.py`
- ✅ Adicionado `CarrinhoAPIView` - API JSON para o carrinho
- ✅ Adicionado `VueAppView` - Serve a aplicação Vue

### `django_caliandra/urls.py`
- ✅ Rota `/app/` - Aplicação Vue
- ✅ Rota `/api/carrinho/` - API do carrinho

### `django_caliandra/settings.py`
- ✅ Adicionado `app/static/app/dist/` ao `STATICFILES_DIRS`

### `app/templates/vue_app.html`
- ✅ Template para servir o Vue (dev e produção)

### `app/vite_helpers.py`
- ✅ Helper para ler manifest.json do Vite

## 🎯 Vantagens da Migração

✅ **Performance**: SPA com transições suaves
✅ **Reatividade**: Estado global com Pinia
✅ **Manutenção**: Componentes reutilizáveis
✅ **Developer Experience**: Hot Module Replacement
✅ **Design Preservado**: 100% fiel ao original Django
✅ **Integração**: Funciona lado a lado com Django

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs do Django
2. Verifique o console do navegador
3. Certifique-se de que ambos os servidores estão rodando (dev mode)
4. Execute `npm run build` após alterações (prod mode)

---

**Desenvolvido com ❤️ mantendo a identidade Caliandra**
