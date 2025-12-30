# 🌸 Caliandra - Frontend Vue.js Completo

## ✅ Status: 100% MIGRADO

**Todas as 9 páginas do Django foram migradas para Vue.js mantendo 100% do design original!**

## 📄 Páginas Disponíveis

| Página | Rota | Django Original | Status |
|--------|------|-----------------|--------|
| Home | `/` | inicio.html | ✅ |
| Login | `/login` | login.html | ✅ |
| Registro | `/registro` | registro.html | ✅ |
| Verificação | `/verificacao` | verificacao.html | ✅ |
| Catálogo | `/catalogo` | catalogo.html | ✅ |
| Carrinho | `/carrinho` | ver_pedido.html | ✅ |
| Perfil | `/perfil` | perfil.html | ✅ |
| Blog | `/blog` | blog.html | ✅ |
| Finalização | `/finalizacao` | finalizacao.html | ✅ |

## 🚀 Como Usar

### Início Rápido

```bash
# 1. Inicie o Django
python manage.py runserver

# 2. Acesse
http://localhost:8000/app/
```

**Todas as páginas estão funcionando!**

### Desenvolvimento com Hot Reload

**Terminal 1:**
```bash
python manage.py runserver
```

**Terminal 2:**
```bash
cd frontend && npm run dev
```

**Acesse:** http://localhost:5173/

## 📋 Funcionalidades Implementadas

### ✅ Páginas Completas
- Hero section (Home)
- Login com validação
- Registro de usuário
- Verificação 2FA com código
- Catálogo de produtos (grid responsivo)
- Carrinho completo (quantidade, remover, total)
- Perfil do usuário (editar dados)
- Blog/Sobre (quem somos, compra coletiva)
- Finalização com QR Code PIX

### ✅ Features
- Conditional header (oculto em login/registro/verificação)
- Navigation guards (rotas protegidas)
- Loading states
- Error handling
- Formatação brasileira (R$)
- Responsive design
- Bootstrap Icons SVG
- Gradientes preservados

## 🔌 APIs Disponíveis

```
GET  /api/carrinho/              # Dados do carrinho
GET  /api/produtos/              # Lista de produtos
GET  /api/perfil/                # Dados do usuário
POST /ajax/atualizar-quantidade/ # Atualizar quantidade
POST /ajax/remover-item/         # Remover item
POST /ajax/esvaziar-carrinho/    # Esvaziar carrinho
```

## 🎨 Design 100% Preservado

- ✅ Cores: #fc9685, #fbaa70, #fffedf, #f0d9d1
- ✅ Fontes: Alexandria (body), Amethysta (headings)
- ✅ Gradientes: linear-gradient(#fbaa70, #ff9f40)
- ✅ Logo: 214x146px
- ✅ Responsivo

## 📊 Bundle Size

```
main.js:  173.21 kB (63.74 kB gzip)
main.css:  10.10 kB (2.47 kB gzip)
Total:    ~183 kB (~66 kB gzip)
```

## 📚 Documentação

- **MIGRATION_COMPLETE.md** - Detalhes completos da migração
- **VUE_INTEGRATION_GUIDE.md** - Guia de integração
- **TECHNICAL_SUMMARY.md** - Resumo técnico com APIs

## 🎯 Teste Rápido

```bash
# 1. Instale dependências (se necessário)
pip install python-dotenv django-cotton crispy-bootstrap5 django-crispy-forms pillow

# 2. Execute o Django
python manage.py runserver

# 3. Abra no navegador
http://localhost:8000/app/

# 4. Navegue pelas páginas
- Clique em "Catálogo" → veja produtos
- Clique no carrinho → veja itens
- Clique em "Blog" → sobre a Caliandra
- Acesse /app/login → formulário de login
```

## 🌸 Caliandra

Compras coletivas de produtos naturais de qualidade por preços acessíveis!

---

**Migração concluída em:** 30/12/2024  
**Status:** ✅ Produção Ready  
**Design:** 🎨 100% Preservado  
**Performance:** 🚀 Otimizado
