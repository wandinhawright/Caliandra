import random
from django.core.management.base import BaseCommand
from app.models import Produto

class Command(BaseCommand):
    help = 'Cadastra produtos de teste no banco de dados'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando o cadastro de produtos de teste...")

        # Limpa os produtos existentes para evitar duplicatas a cada execução
        Produto.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Produtos antigos foram removidos.'))

        produtos_para_criar = [
            {
                'nome': 'PURO GEL DE ALOE 500 ML',
                'descricao': 'Gel de Aloe vera Face + Corpo + Cabelo. Base bioativa sem perfume para protocolos estéticos e de aromaterapia.',
                'valor': 57.18,
                'imagem': 'produtos/placeholder.jpg',
                'marca': 'Livealoe',
                'tipo': 'Multifuncional'
            },
            {
                'nome': 'SHAMPOO FORTALECEDOR 240ML',
                'descricao': 'Previne e trata queda capilar. Estimula o crescimento de novos fios. Nutre e fortalece o bulbo capilar.',
                'valor': 35.50,
                'imagem': 'produtos/placeholder.jpg',
                'marca': 'Livealoe',
                'tipo': 'Cabelo'
            },
            {
                'nome': 'BALSAMO DE GERANIO 30 G',
                'descricao': 'Hidratante facial para a pele madura, normal a seca. Nutre e hidrata até a camada mais profunda da pele.',
                'valor': 48.72,
                'imagem': 'produtos/placeholder.jpg',
                'marca': 'Livealoe',
                'tipo': 'Face'
            },
            {
                'nome': 'OLEO ESSENCIAL DE LAVANDA 15ML',
                'descricao': 'Indicado tanto para pessoas agitadas como deprimidas, o óleo essencial de lavanda traz estabilidade mental e física.',
                'valor': 25.00,
                'imagem': 'produtos/placeholder.jpg',
                'marca': 'Livealoe',
                'tipo': 'Óleos Essenciais'
            },
            {
                'nome': 'DESODORANTE NATURAL ALOE COPAIBA 120ML',
                'descricao': 'Respeita a fisiologia da pele e da axila. Não contém sais de alumínio, não contém antitranspirante.',
                'valor': 30.25,
                'imagem': 'produtos/placeholder.jpg',
                'marca': 'Livealoe',
                'tipo': 'Corpo'
            }
        ]

        for dados_produto in produtos_para_criar:
            Produto.objects.create(**dados_produto)

        self.stdout.write(self.style.SUCCESS(f'{len(produtos_para_criar)} produtos de teste foram cadastrados com sucesso!'))
