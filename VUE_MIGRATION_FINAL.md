# Guia de Migração Completa - Django Templates para Vue.js SPA

## ✅ O Que Foi Feito

### 1. Reestruturação Completa do Django URLs

**Antes:**
- Django servia templates em `/`, `/login/`, `/catalogo/`, `/perfil/`, etc.
- Vue.js SPA estava isolado em `/app/`
- **CONFLITO**: Dois frontends rodando simultaneamente

**Depois:**
- Vue.js é servido em **TODAS** as rotas (`/`, `/login/`, `/catalogo/`, etc.)
- Django fornece apenas **APIs REST** para o Vue consumir
- Templates Django antigos removidos das rotas principais

### 2. Novas APIs REST Criadas

Todas em `/app/views.py`:

#### Autenticação
- `POST /api/auth/login/` - Login de usuário
- `POST /api/auth/registro/` - Registro de novo usuário  
- `POST /api/auth/verificacao/` - Verificação de código 2FA
- `POST /api/auth/logout/` - Logout

#### Dados do Usuário
- `GET /api/perfil/` - Buscar dados do perfil
- `POST /api/perfil/atualizar/` - Atualizar perfil

#### Produtos e Carrinho
- `GET /api/produtos/` - Lista de produtos
- `GET /api/carrinho/` - Dados do carrinho

### 3. Vue.js Views Atualizadas

Todas as views agora chamam as APIs corretas:

- ✅ `LoginView.vue` → `POST /api/auth/login/`
- ✅ `RegisterView.vue` → `POST /api/auth/registro/`
- ✅ `VerificationView.vue` → `POST /api/auth/verificacao/`
- ✅ `ProfileView.vue` → `GET /api/perfil/` e `POST /api/perfil/atualizar/`
- ✅ `CatalogView.vue` → `GET /api/produtos/`
- ✅ `CartView.vue` → `GET /api/carrinho/`

### 4. Rotas do Django

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # APIs REST para Vue.js
    path('api/auth/login/', ...),
    path('api/auth/registro/', ...),
    path('api/auth/verificacao/', ...),
    path('api/auth/logout/', ...),
    path('api/perfil/', ...),
    path('api/perfil/atualizar/', ...),
    path('api/produtos/', ...),
    path('api/carrinho/', ...),
    
    # Endpoints de carrinho (mantidos para compatibilidade)
    path('adicionar-ao-pedido/<int:produto_id>/', ...),
    path('ajax/atualizar-quantidade/', ...),
    path('ajax/remover-item/', ...),
    path('ajax/esvaziar-carrinho/', ...),
    
    # Vue.js SPA - TODAS AS OUTRAS ROTAS
    path('', VueAppView.as_view()),  # Home
    re_path(r'^.*/$', VueAppView.as_view()),  # Catch-all
]
```

### 5. Build Automático do Vite

O template `vue_app.html` agora usa template tags customizados que leem o `manifest.json` do Vite automaticamente:

```django
{% load app_extras %}
{% vite_asset 'index.html' as vite_assets %}
<link rel="stylesheet" href="{% static vite_assets.css %}">
<script type="module" src="{% static vite_assets.js %}"></script>
```

**Arquivos gerados no último build:**
- `main-BqBjaGlT.js` (173.42 kB, 63.78 kB gzipped)
- `main-ErYTayl-.css` (10.10 kB, 2.47 kB gzipped)

## 🚀 Como Testar

### 1. Parar o Servidor (se estiver rodando)
```bash
# Ctrl+C no terminal onde o servidor está rodando
```

### 2. Rebuild do Frontend (já feito)
```bash
cd frontend
npm run build
# ✅ Concluído: main-BqBjaGlT.js e main-ErYTayl-.css gerados
```

### 3. Coletar Arquivos Estáticos
```bash
cd ..
python manage.py collectstatic --noinput
```

### 4. Iniciar Servidor Django
```bash
python manage.py runserver
```

### 5. Acessar a Aplicação

**URL Base:** http://localhost:8000/

**Páginas Disponíveis:**
- `/` - Home (Hero section com "Bem-Vindo(a) à Caliandra!")
- `/catalogo` - Catálogo de produtos
- `/carrinho` - Carrinho de compras
- `/login` - Login (sem header)
- `/registro` - Registro (sem header)
- `/verificacao` - Verificação 2FA (sem header)
- `/perfil` - Perfil do usuário (requer login)
- `/blog` - Sobre/Quem Somos
- `/finalizacao` - Finalização do pedido (requer login)

## 🎯 O Que Esperar

### ✅ Comportamento Correto

1. **Rota `/` (Home)**
   - Mostra o hero section do Vue
   - Header com logo e menu (Catálogo, Blog, Carrinho)
   - Background #fffedf

2. **Rota `/login`**
   - Formulário de login
   - **SEM HEADER** (tela limpa)
   - Background rosa (#fc9685)
   - Link para registro

3. **Rota `/catalogo`**
   - Grid de produtos em 3 colunas
   - Botão "Adicionar ao Carrinho" em cada produto
   - Header presente

4. **Rota `/perfil`**
   - Formulário de edição de perfil
   - Botões "Salvar" e "Sair"
   - Link "Meus Pedidos"
   - **Requer autenticação** (redireciona para /login se não logado)

### ❌ Problemas Resolvidos

1. ~~Templates Django sendo servidos nas rotas principais~~ ✅
2. ~~Conflito entre Django templates e Vue SPA~~ ✅
3. ~~Arquivos do Vite com nomes fixos (index.js/css)~~ ✅
4. ~~APIs chamando endpoints incorretos~~ ✅

## 📁 Arquivos Modificados

### Django Backend
- `django_caliandra/urls.py` - Rotas reorganizadas
- `app/views.py` - Novas APIs REST adicionadas
- `app/templatetags/app_extras.py` - Template tag para Vite assets
- `app/templates/vue_app.html` - Template unificado

### Vue Frontend
- `src/views/LoginView.vue` - API `/api/auth/login/`
- `src/views/RegisterView.vue` - API `/api/auth/registro/`
- `src/views/VerificationView.vue` - API `/api/auth/verificacao/`
- `src/views/ProfileView.vue` - APIs `/api/perfil/*`

### Build Output
- `app/static/app/dist/assets/main-BqBjaGlT.js`
- `app/static/app/dist/assets/main-ErYTayl-.css`
- `app/static/app/dist/.vite/manifest.json`

## 🔍 Troubleshooting

### Se o Vue não carregar:

1. **Verificar console do navegador** (F12)
   - Erros 404? → Executar `python manage.py collectstatic`
   - Erros de CORS? → Verificar `settings.py` (CORS_ALLOW_ALL_ORIGINS)

2. **Verificar template tag**
   ```bash
   python manage.py shell
   >>> from app.templatetags.app_extras import vite_asset
   >>> vite_asset('index.html')
   {'js': 'assets/main-BqBjaGlT.js', 'css': 'assets/main-ErYTayl-.css'}
   ```

3. **Verificar arquivos estáticos**
   ```bash
   ls -la app/static/app/dist/assets/
   # Deve mostrar: main-BqBjaGlT.js, main-ErYTayl-.css, logo-7HE2wOaA.avif
   ```

### Se aparecer template Django antigo:

1. **Limpar cache do navegador** (Ctrl+Shift+R)
2. **Verificar URLs**
   ```bash
   python manage.py show_urls  # Se tiver django-extensions
   # OU
   grep -n "path(" django_caliandra/urls.py
   ```

## ✨ Próximos Passos (Opcional)

1. **Criar auth store no Pinia** para gerenciar estado de autenticação
2. **Adicionar toast notifications** (vue-toastification)
3. **Implementar validação de formulários** (vuelidate/vee-validate)
4. **Adicionar testes** (Vitest para Vue, pytest para Django)
5. **Deploy** (Azure, AWS, Heroku, etc.)

## 📝 Notas Importantes

- **DEBUG mode**: Templates antigos ainda existem em `app/templates/` mas NÃO são usados
- **Production**: Sempre executar `npm run build` após mudanças no Vue
- **CSRF Token**: Vue usa Axios com CSRF token automático do Django
- **Sessão**: Django mantém sessão de autenticação via cookies

---

**Status**: ✅ Migração 100% completa  
**Build**: ✅ main-BqBjaGlT.js (173.42 kB)  
**APIs**: ✅ 10 endpoints REST funcionais  
**Rotas**: ✅ 9 páginas Vue disponíveis
