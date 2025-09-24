# Comandos Úteis e Checklist - Projeto Caliandra

## 🚀 Comandos Git para Issues

### Iniciando trabalho em uma issue
```bash
# Crear branch para a issue
git checkout -b feature/issue-1-autenticacao
git checkout -b feature/issue-2-catalogo
git checkout -b feature/issue-3-carrinho
# etc...

# Fazer commit referenciando a issue
git commit -m "implementa validação client-side no login

Refs #1"

# Push da branch
git push -u origin feature/issue-1-autenticacao
```

### Finalizando uma issue
```bash
# Commit final referenciando o fechamento
git commit -m "feat: finaliza sistema de autenticação

- Implementa recuperação de senha
- Adiciona validações client-side  
- Melhora feedback visual
- Configura redirecionamentos

Closes #1"

# Criar Pull Request via CLI (GitHub CLI)
gh pr create --title "Aprimoramento do Sistema de Autenticação" --body "Implementa todas as melhorias definidas na issue #1"
```

---

## 📋 Checklist de Início de Sprint

### Antes de começar
- [ ] Revisar planejamento do sprint
- [ ] Criar branch específica para a issue
- [ ] Ler completamente a descrição da issue
- [ ] Entender critérios de aceitação
- [ ] Identificar dependências técnicas

### Durante o desenvolvimento
- [ ] Fazer commits pequenos e frequentes
- [ ] Testar funcionalidades localmente
- [ ] Atualizar documentação se necessário
- [ ] Seguir padrões de código estabelecidos
- [ ] Implementar tratamento de erros

### Antes de finalizar
- [ ] Executar todos os testes
- [ ] Verificar responsividade (mobile/desktop)
- [ ] Testar em diferentes navegadores
- [ ] Revisar código próprio
- [ ] Atualizar tracking de progresso

---

## 🔧 Comandos Django Úteis

### Durante desenvolvimento
```bash
# Rodar servidor de desenvolvimento
python manage.py runserver

# Criar e aplicar migrações
python manage.py makemigrations
python manage.py migrate

# Criar superuser (se necessário)
python manage.py createsuperuser

# Executar testes
python manage.py test

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Shell do Django para debugging
python manage.py shell
```

### Para Issues específicas
```bash
# Issue #1 - Testar autenticação
python manage.py test app.tests.test_authentication

# Issue #9 - Executar todos os testes
python manage.py test --verbosity=2 --keepdb

# Issue #7 - Backup antes da migração
python manage.py dumpdata > backup_antes_migracao.json
```

---

## 📊 Comandos de Monitoramento

### Performance (Issue #8)
```bash
# Verificar dependências desatualizadas
pip list --outdated

# Analisar tamanho do banco
ls -lh db.sqlite3

# Verificar uso de memória
ps aux | grep python
```

### Segurança (Issue #8)
```bash
# Verificar vulnerabilidades
pip audit

# Verificar configurações Django
python manage.py check --deploy
```

---

## 🎨 Frontend - Comandos CSS/JS

### Para Issues #2, #3, #4 (Frontend)
```bash
# Compilar assets (se usando SASS)
sass app/static/app/scss/main.scss app/static/app/css/main.css --watch

# Minificar CSS (produção)
cleancss -o app/static/app/css/main.min.css app/static/app/css/main.css

# Verificar JavaScript
eslint app/static/app/js/

# Comprimir imagens
imagemin app/static/app/img/*.jpg --out-dir=app/static/app/img/compressed/
```

---

## 📧 Templates de Email (Issue #5)

### Testando emails localmente
```bash
# Console backend (desenvolvimento)
# Adicionar no settings.py:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Arquivo backend (salvar emails em arquivos)
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/tmp/app-messages'
```

---

## 🧪 Testing (Issue #9)

### Comandos de teste
```bash
# Executar testes específicos
python manage.py test app.tests.test_models
python manage.py test app.tests.test_views
python manage.py test app.tests.test_forms

# Executar com cobertura
coverage run --source='.' manage.py test
coverage report
coverage html

# Teste de performance
python manage.py test --debug-mode --verbosity=2
```

---

## 📝 Checklist Definition of Done

### Para cada Issue
- [ ] Funcionalidade implementada conforme especificação
- [ ] Código revisado e limpo
- [ ] Testes passando (quando aplicável)
- [ ] Documentação atualizada
- [ ] Responsividade testada
- [ ] Cross-browser testado (Chrome, Firefox, Safari)
- [ ] Performance aceitável
- [ ] Sem vulnerabilidades de segurança
- [ ] Pull Request criado e aprovado
- [ ] Merge realizado
- [ ] Issue marcada como concluída

---

## 🏷️ Sistema de Labels Sugerido

### Criar labels no GitHub
```bash
# Via GitHub CLI
gh label create "sprint-1" --color "0075ca" --description "Sprint 1 tasks"
gh label create "sprint-2" --color "0075ca" --description "Sprint 2 tasks"  
gh label create "sprint-3" --color "0075ca" --description "Sprint 3 tasks"
gh label create "high-priority" --color "d73a49" --description "High priority"
gh label create "medium-priority" --color "fbca04" --description "Medium priority"
gh label create "low-priority" --color "28a745" --description "Low priority"
gh label create "frontend" --color "7057ff" --description "Frontend related"
gh label create "backend" --color "008672" --description "Backend related"
gh label create "security" --color "b60205" --description "Security related"
gh label create "performance" --color "0052cc" --description "Performance related"
```

---

## 🚨 Troubleshooting Comum

### Problemas frequentes e soluções
```bash
# Problema: Migrações conflitantes
python manage.py migrate --fake-initial

# Problema: Arquivos estáticos não carregam
python manage.py collectstatic --clear

# Problema: Permissões de arquivo
chmod +x manage.py

# Problema: Conflitos de dependência
pip freeze > requirements_old.txt
pip install --upgrade pip
pip install -r requirements.txt
```

---

*Documento criado em: 23 de setembro de 2025*
