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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app.views import (
    FinalizacaoView, InicioView, LoginView, LogoutView, VerifyCodeView, 
    CatalogoView, AdicionarAoPedidoView, VerPedidoView, FinalizarPedidoView,
    AtualizarQuantidadeView, RemoverItemView, EsvaziarCarrinhoView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', InicioView.as_view(), name='inicio'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verifica-codigo/', VerifyCodeView.as_view(), name='verifica_codigo'),
    path('catalogo/', CatalogoView.as_view(), name='catalogo'),
    path('adicionar-ao-pedido/<int:produto_id>/', AdicionarAoPedidoView.as_view(), name='adicionar_ao_pedido'),
    path('ver-pedido/', VerPedidoView.as_view(), name='ver_pedido'),
    path('finalizar-pedido/', FinalizarPedidoView.as_view(), name='finalizar_pedido'),
    path('finalizacao/', FinalizacaoView.as_view(), name='finalizacao'),
    # AJAX endpoints for cart management
    path('ajax/atualizar-quantidade/', AtualizarQuantidadeView.as_view(), name='atualizar_quantidade'),
    path('ajax/remover-item/', RemoverItemView.as_view(), name='remover_item'),
    path('ajax/esvaziar-carrinho/', EsvaziarCarrinhoView.as_view(), name='esvaziar_carrinho'),
]

# Servir arquivos estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
