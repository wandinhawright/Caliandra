from django.contrib import admin
from .models import Usuario, Pedido, Produto
# Register your models here.
class PedidoInline(admin.TabularInline):  # ou StackedInline para visual diferente
    model = Pedido
    extra = 1  # quantos "pedidos vazios" aparecem para cadastrar rápido

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    inlines = [PedidoInline]

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    pass

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    pass
