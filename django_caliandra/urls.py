"""
URL configuration for django_caliandra project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from app.views import (
    LogoutView, AdicionarAoPedidoView, FinalizarPedidoView,
    AtualizarQuantidadeView, RemoverItemView, EsvaziarCarrinhoView,
    CarrinhoAPIView, VueAppView, ProdutosAPIView, PerfilAPIView, 
    RegistroAPIView, LoginAPIView, VerificationAPIView, PerfilUpdateAPIView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Endpoints para o Vue.js
    path('api/carrinho/', CarrinhoAPIView.as_view(), name='api_carrinho'),
    path('api/produtos/', ProdutosAPIView.as_view(), name='api_produtos'),
    path('api/perfil/', PerfilAPIView.as_view(), name='api_perfil'),
    path('api/perfil/atualizar/', PerfilUpdateAPIView.as_view(), name='api_perfil_update'),
    path('api/auth/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/auth/registro/', RegistroAPIView.as_view(), name='api_registro'),
    path('api/auth/verificacao/', VerificationAPIView.as_view(), name='api_verificacao'),
    path('api/auth/logout/', LogoutView.as_view(), name='api_logout'),
    
    # Endpoints de Carrinho (mantidos para compatibilidade)
    path('adicionar-ao-pedido/<int:produto_id>/', AdicionarAoPedidoView.as_view(), name='adicionar_ao_pedido'),
    path('finalizar-pedido/', FinalizarPedidoView.as_view(), name='finalizar_pedido'),
    path('ajax/atualizar-quantidade/', AtualizarQuantidadeView.as_view(), name='atualizar_quantidade'),
    path('ajax/remover-item/', RemoverItemView.as_view(), name='remover_item'),
    path('ajax/esvaziar-carrinho/', EsvaziarCarrinhoView.as_view(), name='esvaziar_carrinho'),
    
    # Vue.js SPA - Serve para TODAS as rotas (exceto admin e api)
    path('', VueAppView.as_view(), name='vue_app'),
    re_path(r'^.*/$', VueAppView.as_view()),  # Catch-all para todas as subrotas
]

# Servir arquivos estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
