from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

# Create your models here.
class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=255)
    
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    valor= models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/')
    marca = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)

class Pedido(models.Model):
    produtos = models.ManyToManyField(Produto)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        Usuario,  # ou User se estiver usando o padrão
        on_delete=models.CASCADE,
        related_name="pedidos"
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    situacao = models.CharField(default='PENDENTE',choices=[
        ('PENDENTE', 'Pendente'),
        ('FEITO', 'Feito'),
        ('FINALIZADO', 'Finalizado')
    ])
