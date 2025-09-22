# app/admin.py
from django.contrib import admin
from .models import Usuario, Pedido, Produto, ItemPedido

class PedidoInline(admin.TabularInline):
    model = Pedido
    extra = 0 # Não mostrar formulários extras

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    inlines = [PedidoInline]

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    pass

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    readonly_fields = ('produto', 'quantidade') # Apenas visualização
    extra = 0

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'data', 'situacao', 'total')
    list_filter = ('situacao', 'data')
    inlines = [ItemPedidoInline]

    # ESTA É A FUNÇÃO CHAVE!
    def get_queryset(self, request):
        # Pega o queryset padrão
        qs = super().get_queryset(request)
        # Filtra para excluir pedidos com situação 'CARRINHO'
        return qs.exclude(situacao='CARRINHO')