# Correção de Carregamento de Assets Vue no Django

## Problema Identificado

Quando você acessava o app pelo Django runserver (`http://localhost:8000/app/`), o frontend Vue não estava sendo carregado corretamente porque o template estava tentando carregar arquivos com nomes fixos (`index.css` e `index.js`), mas o Vite gera arquivos com hashes no nome (exemplo: `main-CZXgx3BJ.js` e `main-D_jj3VGj.css`).

## Solução Implementada

### 1. Template Tag Customizado

Criado um template tag Django em `app/templatetags/app_extras.py` que:
- Lê o arquivo `manifest.json` gerado pelo Vite
- Extrai os nomes reais dos arquivos JavaScript e CSS
- Retorna os caminhos corretos para o template

### 2. Template Vue App Atualizado

O template `app/templates/vue_app.html` agora:
- Carrega o template tag com `{% load app_extras %}`
- Usa `{% vite_asset 'index.html' as vite_assets %}` para obter os caminhos
- Referencia dinamicamente os arquivos: `{% static vite_assets.css %}` e `{% static vite_assets.js %}`

### 3. Estrutura Criada

```
app/
├── templatetags/
│   ├── __init__.py
│   └── app_extras.py     # Template tag customizado
└── templates/
    └── vue_app.html       # Template atualizado
```

## Como Funciona

1. **Build do Vue**: `npm run build` gera arquivos com hash no nome
2. **Manifest.json**: Vite cria um manifest mapeando entry points para arquivos reais
3. **Template Tag**: Lê o manifest e retorna os nomes corretos
4. **Template**: Usa os nomes dinâmicos para carregar os assets

## Resultado

✅ O frontend Vue agora carrega corretamente no Django  
✅ Não é necessário atualizar manualmente os nomes dos arquivos após cada build  
✅ Funciona em desenvolvimento (com Vite dev server) e produção (com arquivos buildados)

## Como Testar

1. **Pare o servidor Django se estiver rodando** (Ctrl+C)
2. **Execute o build do Vue**:
   ```bash
   cd frontend
   npm run build
   ```

3. **Inicie o servidor Django**:
   ```bash
   cd ..
   python manage.py runserver
   ```

4. **Acesse no navegador**:
   ```
   http://localhost:8000/app/
   ```

Agora você verá o frontend Vue completo com todas as páginas funcionando corretamente! 🎉

## Páginas Disponíveis

- `/app/` - Home (página inicial)
- `/app/#/catalogo` - Catálogo de produtos
- `/app/#/carrinho` - Carrinho de compras
- `/app/#/login` - Login
- `/app/#/registro` - Registro
- `/app/#/perfil` - Perfil do usuário
- `/app/#/blog` - Sobre/Blog
- `/app/#/verificacao` - Verificação 2FA
- `/app/#/finalizacao` - Finalização do pedido
