# Configuração de Arquivos Estáticos - Projeto Caliandra

## Estrutura dos Arquivos Estáticos

```
app/static/app/
├── css/
│   ├── bootstrap.min.css           # Bootstrap CSS
│   ├── bss-overrides.css          # Sobrescritas do Bootstrap
│   ├── Navbar-Centered-Links-icons.css  # Estilos de ícones
│   └── custom-styles.css          # Estilos customizados do projeto
├── js/
│   └── bootstrap.min.js           # Bootstrap JavaScript
├── img/
│   └── ca3pia-de-lgcaliandra_v3-1---editado-YZ9j93rw22hp8GnK.avif  # Logo
└── fonts/
    ├── fontawesome-all.min.css    # FontAwesome CSS
    └── fa-*.{eot,svg,ttf,woff,woff2}  # Arquivos de fonte FontAwesome
```

## Como Usar em Templates

### 1. Template Base (base.html)
Criamos um template base que pode ser reutilizado:

```django
{% extends 'base.html' %}

{% block title %}Sua Página - Caliandra{% endblock %}

{% block content %}
    <!-- Seu conteúdo aqui -->
{% endblock %}
```

### 2. Carregando Arquivos Estáticos
No início de qualquer template, carregue os arquivos estáticos:

```django
{% load static %}

<!-- CSS -->
<link rel="stylesheet" href="{% static 'app/css/bootstrap.min.css' %}">
<link rel="stylesheet" href="{% static 'app/css/custom-styles.css' %}">

<!-- JavaScript -->
<script src="{% static 'app/js/bootstrap.min.js' %}"></script>

<!-- Imagens -->
<img src="{% static 'app/img/ca3pia-de-lgcaliandra_v3-1---editado-YZ9j93rw22hp8GnK.avif' %}" alt="Logo">
```

### 3. Adicionando CSS/JS Específico de Página
Use os blocos `extra_css` e `extra_js` no template base:

```django
{% extends 'base.html' %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'app/css/sua-pagina.css' %}">
{% endblock %}

{% block extra_js %}
<script src="{% static 'app/js/sua-pagina.js' %}"></script>
{% endblock %}
```

## Configurações Realizadas

### settings.py
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'app' / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### urls.py
```python
from django.conf import settings
from django.conf.urls.static import static

# Servir arquivos estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Comandos Úteis

### Coletar arquivos estáticos para produção:
```bash
python3 manage.py collectstatic
```

### Encontrar arquivos estáticos conflitantes:
```bash
python3 manage.py findstatic nome-do-arquivo.css
```

## Paleta de Cores do Projeto

As seguintes cores estão configuradas no custom-styles.css:

- **Primary**: #fbf793 (amarelo claro)
- **Secondary**: #c0f79f (verde claro)  
- **Success**: #ffc368 (laranja claro)
- **Body Color**: #212929 (cinza escuro)

## Próximos Passos

1. Atualize seus outros templates para usar o template base
2. Adicione CSS específico para cada página conforme necessário
3. Para produção, configure um servidor web (nginx/apache) para servir arquivos estáticos
4. Considere usar um CDN para melhor performance

## Exemplos de Uso

### Botões com as cores do projeto:
```html
<button class="btn btn-primary">Botão Primário</button>
<button class="btn btn-secondary">Botão Secundário</button>
<button class="btn btn-success">Botão Sucesso</button>
```

### Ícones FontAwesome:
```html
<i class="fas fa-user"></i>
<i class="far fa-heart"></i>
<i class="fab fa-github"></i>
```
