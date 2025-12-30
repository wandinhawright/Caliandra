from datetime import datetime, timedelta
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import ItemPedido, Usuario, Produto, Pedido
from .forms import LoginForm, RegistroForm, VerificationCodeForm, CheckoutForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
import random
import json
# Create your views here.
class InicioView(View):
    def get(self, request):
        return render(request, 'inicio.html')

class LoginView(View):
    def get(self, request):
        action = request.GET.get("action", "login")
        
        if action == "registrar":
            return render(request, 'registro.html', {'form': RegistroForm()})
        else:
            form = LoginForm()
            return render(request, 'login.html', {'form': form})
    
    def post(self, request):
        action = request.POST.get("action", "login")
        
        if action == "registrar":
            form = RegistroForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')

                if Usuario.objects.filter(email=email).exists():
                    return render(request, 'registro.html', {
                        'form': form,
                        'error': 'Este email já está cadastrado.'
                    })
                if form.cleaned_data.get('password') != form.cleaned_data.get('confirmar_password'):
                    return render(request, 'registro.html', {
                        'form': form,
                        'error': 'As senhas não coincidem.'
                    })
                # Armazena os dados do formulário na sessão para usar após a verificação
                request.session['registration_data'] = form.cleaned_data
                
                # Gera e envia o código de verificação
                verification_code = random.randint(100000, 999999)
                request.session['verification_code'] = verification_code
                request.session['verification_code_expires'] = (datetime.now() + timedelta(minutes=10)).isoformat()

                try:
                    send_mail(
                        'Código de Verificação de Cadastro',
                        f'Olá! Seu código para finalizar o cadastro é: {verification_code}',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Enviamos um código de verificação para o seu e-mail para finalizar o cadastro.')
                except Exception as e:
                    messages.error(request, f'Não foi possível enviar o e-mail de verificação. Erro: {e}')
                    return render(request, 'registro.html', {'form': form})

                return redirect('verificacao')
            else:
                 return render(request, 'registro.html', {'form': form})


        else: # action == "login"
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                usuario = authenticate(request, email=email, password=password)

                if usuario is not None:
                    # Login direto, sem verificação em duas etapas
                    login(request, usuario)
                    return redirect('inicio')
                else:
                    return render(request, 'login.html', {
                        'form': form,
                        'error': 'Credenciais inválidas'
                    })
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Formulário inválido.'})


class VerifyCodeView(View):
    """
    Esta view lida com a verificação do código para FINALIZAR O REGISTRO.
    """
    def get(self, request):
        form = VerificationCodeForm()
        return render(request, 'verificacao.html', {'form': form})

    def post(self, request):
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            user_code = form.cleaned_data.get('code')
            
            # Recupera os dados da sessão
            stored_code = request.session.get('verification_code')
            expires_str = request.session.get('verification_code_expires')
            registration_data = request.session.get('registration_data')

            if not all([stored_code, expires_str, registration_data]):
                 messages.error(request, 'Sua sessão expirou. Por favor, inicie o cadastro novamente.')
                 return redirect('login' + '?action=registrar')

            # Checa se o código não expirou
            expiration_time = datetime.fromisoformat(expires_str)
            if datetime.now() > expiration_time:
                messages.error(request, 'O código de verificação expirou. Por favor, inicie o cadastro novamente.')
                return redirect('login' + '?action=registrar')

            # Checa se o código está correto
            if int(user_code) == stored_code:
                # Código correto! Cria o usuário com os dados da sessão.
                try:
                    user = Usuario.objects.create_user(
                        email=registration_data['email'],
                        password=registration_data['password'],
                        nome=registration_data['nome'],
                        telefone=registration_data['telefone'],
                       
                    )
                    login(request, user)
                    
                    # Limpa os dados da sessão após o sucesso
                    del request.session['verification_code']
                    del request.session['verification_code_expires']
                    del request.session['registration_data']

                    messages.success(request, 'Cadastro realizado com sucesso!')
                    return redirect('inicio')
                except Exception as e:
                    messages.error(request, f'Ocorreu um erro ao criar sua conta: {e}. Tente novamente.')
                    return redirect('login' + '?action=registrar')
            else:
                messages.error(request, 'Código de verificação inválido.')
                return render(request, 'verificacao.html', {'form': form})
        else:
            return render(request, 'verificacao.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        """Faz logout do usuário e redireciona para a página de login"""
        logout(request)
        return redirect('inicio')
    
    def post(self, request):
        """Permite logout via POST também"""
        logout(request)
        return redirect('inicio')
    
class CatalogoView(View):
    def get(self, request):
        produtos = Produto.objects.all()
        return render(request, 'catalogo.html', {'produtos': produtos})

class AdicionarAoPedidoView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def post(self, request, produto_id):
        produto = Produto.objects.get(id=produto_id)
        
        # Pega ou cria um carrinho para o usuário
        pedido, criado = Pedido.objects.get_or_create(
            usuario=request.user,
            situacao='CARRINHO'
        )
        
        # Pega ou cria o item no pedido e incrementa a quantidade
        item_pedido, item_criado = ItemPedido.objects.get_or_create(
            pedido=pedido,
            produto=produto
        )
        
        if not item_criado:
            item_pedido.quantidade += 1
            item_pedido.save()

        return redirect('catalogo')


class VerPedidoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        try:
            # Busca pelo carrinho do usuário
            pedido = Pedido.objects.get(usuario=request.user, situacao='CARRINHO')
            # Pega todos os itens associados a esse carrinho
            itens = ItemPedido.objects.filter(pedido=pedido)
            
            # Calcula o total
            total = 0
            for item in itens:
                total += item.get_total_item_price()
            pedido.total = total
            pedido.save()

        except Pedido.DoesNotExist:
            itens = None
            pedido = None
        
        # Criar o formulário de checkout
        form = CheckoutForm()
        
        return render(request, 'ver_pedido.html', {
            'pedido': pedido, 
            'itens': itens,
            'form': form
        })

class FinalizarPedidoView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request):
        """
        Permite finalizar pedido diretamente via GET quando clica no botão.
        Simplifica o fluxo: usuário clica em "Finalizar Pedido" e pronto!
        """
        try:
            pedido = Pedido.objects.get(usuario=request.user, situacao='CARRINHO')
            
            # Verifica se o carrinho tem itens
            if not pedido.itempedido_set.exists():
                messages.warning(request, 'Seu carrinho está vazio.')
                return redirect('ver_pedido')
            
            # Muda a situação para "FEITO", transformando o carrinho em um pedido real
            pedido.situacao = 'FEITO'
            pedido.save()
            
            # Mensagem de sucesso (usa o ID do pedido como número)
            messages.success(request, f'Seu pedido #{pedido.id} foi finalizado com sucesso!')
            
            try:
                resultado = send_mail(
                    subject=f'Pedido #{pedido.id} - Compra Coletiva Caliandra',
                    message=f'Olá {pedido.usuario.nome}!\n\nSeu pedido #{pedido.id} foi recebido com sucesso.\n\nTotal: R$ {pedido.total}\n\nAcompanhe o status do seu pedido através do nosso WhatsApp.\n\nObrigado por participar da nossa compra coletiva!',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[pedido.usuario.email],
                    fail_silently=False,  # Mostra erros se houver
                )
            except Exception as e:
                pass
            
            return redirect('finalizacao')
            
        except Pedido.DoesNotExist:
            messages.error(request, 'Você não tem um carrinho ativo para finalizar.')
            return redirect('ver_pedido')
    
    def post(self, request):
        """
        Mantém compatibilidade com POST caso haja formulário no futuro.
        Por enquanto, apenas chama o GET.
        """
        return self.get(request)
class FinalizacaoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        # Busca pelo último pedido finalizado do usuário
        try:
            pedido = Pedido.objects.filter(
                usuario=request.user, 
                situacao='FEITO'
            ).order_by('-data').first()
            
            if pedido:
                itens = ItemPedido.objects.filter(pedido=pedido)
                return render(request, 'finalizacao.html', {
                    'pedido': pedido,
                    'itens': itens
                })
            else:
                messages.warning(request, 'Nenhum pedido encontrado.')
                return redirect('catalogo')
                
        except Exception as e:
            messages.error(request, 'Erro ao carregar informações do pedido.')
            return redirect('catalogo')

class AtualizarQuantidadeView(LoginRequiredMixin, View):
    """View para atualizar quantidade de item no carrinho via AJAX"""
    login_url = '/login/'
    
    def post(self, request):
        try:
            # Valida Content-Type
            if request.content_type != 'application/json':
                return JsonResponse({
                    'success': False, 
                    'error': 'Content-Type deve ser application/json'
                }, status=400)
            
            data = json.loads(request.body)
            item_id = data.get('item_id')
            nova_quantidade = data.get('quantidade')
            
            # Validações
            if not item_id:
                return JsonResponse({
                    'success': False, 
                    'error': 'item_id é obrigatório'
                }, status=400)
                
            try:
                nova_quantidade = int(nova_quantidade)
            except (TypeError, ValueError):
                return JsonResponse({
                    'success': False, 
                    'error': 'Quantidade deve ser um número válido'
                }, status=400)
            
            if nova_quantidade < 1:
                return JsonResponse({
                    'success': False, 
                    'error': 'Quantidade deve ser maior que zero'
                }, status=400)
            
            if nova_quantidade > 99:
                return JsonResponse({
                    'success': False, 
                    'error': 'Quantidade máxima é 99'
                }, status=400)
            
            # Busca o item do pedido
            item = get_object_or_404(
                ItemPedido, 
                id=item_id, 
                pedido__usuario=request.user, 
                pedido__situacao='CARRINHO'
            )
            
            # Atualiza a quantidade
            item.quantidade = nova_quantidade
            item.save()
            
            # Recalcula o total do pedido
            pedido = item.pedido
            total = sum(item.get_total_item_price() for item in pedido.itempedido_set.all())
            pedido.total = total
            pedido.save()
            
            return JsonResponse({
                'success': True,
                'item_total': float(item.get_total_item_price()),
                'pedido_total': float(pedido.total),
                'quantidade': item.quantidade
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False, 
                'error': 'JSON inválido'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': 'Erro interno do servidor'
            }, status=500)

class RemoverItemView(LoginRequiredMixin, View):
    """View para remover item do carrinho via AJAX"""
    login_url = '/login/'
    
    def post(self, request):
        try:
            # Valida Content-Type
            if request.content_type != 'application/json':
                return JsonResponse({
                    'success': False, 
                    'error': 'Content-Type deve ser application/json'
                }, status=400)
            
            data = json.loads(request.body)
            item_id = data.get('item_id')
            
            if not item_id:
                return JsonResponse({
                    'success': False, 
                    'error': 'item_id é obrigatório'
                }, status=400)
            
            # Busca e remove o item
            item = get_object_or_404(
                ItemPedido, 
                id=item_id, 
                pedido__usuario=request.user, 
                pedido__situacao='CARRINHO'
            )
            pedido = item.pedido
            produto_nome = item.produto.nome
            item.delete()
            
            # Recalcula o total do pedido
            total = sum(item.get_total_item_price() for item in pedido.itempedido_set.all())
            pedido.total = total
            pedido.save()
            
            return JsonResponse({
                'success': True,
                'pedido_total': float(pedido.total),
                'items_count': pedido.itempedido_set.count(),
                'message': f'{produto_nome} removido com sucesso'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False, 
                'error': 'JSON inválido'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': 'Erro interno do servidor'
            }, status=500)

class EsvaziarCarrinhoView(LoginRequiredMixin, View):
    """View para esvaziar carrinho via AJAX"""
    login_url = '/login/'
    
    def post(self, request):
        try:
            # Busca o carrinho do usuário
            pedido = get_object_or_404(Pedido, usuario=request.user, situacao='CARRINHO')
            
            # Conta itens antes de remover
            items_count = pedido.itempedido_set.count()
            
            if items_count == 0:
                return JsonResponse({
                    'success': False,
                    'error': 'Carrinho já está vazio'
                }, status=400)
            
            # Remove todos os itens
            pedido.itempedido_set.all().delete()
            
            # Zera o total
            pedido.total = 0
            pedido.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Carrinho esvaziado com sucesso!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': 'Erro interno do servidor'
            }, status=500)
            
class PerfilView(LoginRequiredMixin, View):
    
    login_url = '/login/'

    def get(self, request):
        return render(request, 'perfil.html', {'usuario': request.user})

    def post(self, request):
        usuario = request.user
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')

        # Atualiza os campos do usuário
        usuario.nome = nome
        usuario.telefone = telefone
        usuario.endereco = endereco
        usuario.save()

        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil') 
    
class BlogView(View):
    def get(self, request):
        return render(request, 'blog.html')  

class RegistroView(View):
    def get(self, request):
        form = RegistroForm()
        return render(request, 'registro.html', {'form': form})
    
    