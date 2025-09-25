from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Produto, Pedido, ItemPedido
from .forms import CheckoutForm

User = get_user_model()

class CheckoutSystemTestCase(TestCase):
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            email='test@test.com',
            nome='Test User',
            telefone='(61) 99999-9999',
            endereco='Test Address',
            password='testpass123'
        )
        
        self.produto = Produto.objects.create(
            nome='Test Product',
            descricao='Test description',
            valor=10.50,
            marca='Test Brand',
            tipo='Test Type'
        )
        
        self.client = Client()
        
    def test_checkout_form_validation(self):
        """Test checkout form validations."""
        # Test empty form (should be valid as no fields are required)
        form_data = {}
        form = CheckoutForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_order_flow(self):
        """Test complete order flow."""
        # Login
        self.client.login(email='test@test.com', password='testpass123')
        
        # Create cart
        pedido = Pedido.objects.create(usuario=self.user, situacao='CARRINHO')
        ItemPedido.objects.create(pedido=pedido, produto=self.produto, quantidade=2)
        
        # Access checkout page
        response = self.client.get(reverse('ver_pedido'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertContains(response, 'Finalizar Pedido')
        
        # Submit checkout form (empty form should work)
        form_data = {}
        
        response = self.client.post(reverse('finalizar_pedido'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect to confirmation
        
        # Check order was finalized
        pedido.refresh_from_db()
        self.assertEqual(pedido.situacao, 'FEITO')
        self.assertEqual(pedido.endereco_entrega, self.user.endereco)  # Should use user's address
        self.assertIsNone(pedido.cep)  # No separate CEP field
        self.assertIsNone(pedido.observacoes)  # No observations
        self.assertIsNotNone(pedido.numero_pedido)
        
        # Access confirmation page
        response = self.client.get(reverse('finalizacao'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pedido Confirmado')
    def test_empty_cart_checkout(self):
        """Test checkout with empty cart."""
        self.client.login(email='test@test.com', password='testpass123')
        
        response = self.client.get(reverse('ver_pedido'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'carrinho está vazio')

class OrderModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            nome='Test User',
            telefone='(61) 99999-9999',
            endereco='Test Address',
            password='testpass123'
        )
        
    def test_order_number_generation(self):
        """Test automatic order number generation."""
        # Create order
        pedido = Pedido.objects.create(
            usuario=self.user,
            situacao='CARRINHO',
            total=100.00
        )
        
        # Order number should not be generated for CARRINHO
        self.assertIsNone(pedido.numero_pedido)
        
        # Finalize order
        pedido.situacao = 'FEITO'
        pedido.save()
        
        # Order number should be generated
        self.assertIsNotNone(pedido.numero_pedido)
        self.assertTrue(pedido.numero_pedido.startswith('CAL'))
        
    def test_order_total_calculation(self):
        """Test order total calculation."""
        produto1 = Produto.objects.create(
            nome='Product 1', valor=10.00, marca='Test', tipo='Test'
        )
        produto2 = Produto.objects.create(
            nome='Product 2', valor=20.50, marca='Test', tipo='Test'
        )
        
        pedido = Pedido.objects.create(usuario=self.user, situacao='CARRINHO')
        
        item1 = ItemPedido.objects.create(pedido=pedido, produto=produto1, quantidade=2)
        item2 = ItemPedido.objects.create(pedido=pedido, produto=produto2, quantidade=1)
        
        # Test item total calculation
        self.assertEqual(item1.get_total_item_price(), 20.00)  # 10.00 * 2
        self.assertEqual(item2.get_total_item_price(), 20.50)  # 20.50 * 1
