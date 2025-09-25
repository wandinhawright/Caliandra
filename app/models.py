from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from PIL import Image

# Create your models here.
class UsuarioManager(UserManager):
    """Manager simples que apenas ajusta os métodos para usar email"""
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=255)
    
    username = None  # Remove o campo username completamente
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']
    
    objects = UsuarioManager()
    
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    valor= models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/')
    marca = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)

class ItemPedido(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def get_total_item_price(self):
        return self.quantidade * self.produto.valor

class Pedido(models.Model):
    produtos = models.ManyToManyField(Produto, through=ItemPedido, related_name='pedidos_item')
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="pedidos"
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Informações de entrega
    endereco_entrega = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    
    # NOVO CAMPO para diferenciar carrinho de pedido
    situacao = models.CharField(
        max_length=20,
        default='CARRINHO',
        choices=[
            ('CARRINHO', 'Carrinho'), # Carrinho ativo, não visível para admin
            ('FEITO', 'Feito'),       # Pedido finalizado, visível para admin
            ('FINALIZADO', 'Finalizado') # Pedido entregue/concluído
        ]
    )
    
    # Número do pedido para tracking
    numero_pedido = models.CharField(max_length=20, blank=True, null=True, unique=True)
    
    def save(self, *args, **kwargs):
        # Gerar número do pedido quando finalizado
        if self.situacao == 'FEITO' and not self.numero_pedido:
            import random
            import string
            self.numero_pedido = f"CAL{self.id or random.randint(1000, 9999)}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=4))}"
        super().save(*args, **kwargs)