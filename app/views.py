from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Usuario, Produto, Pedido
from .forms import LoginForm, RegistroForm, VerificationCodeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
import random
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

                return redirect('verifica_codigo')
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
        return render(request, 'verifica_codigo.html', {'form': form})

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
                        endereco=registration_data['endereco']
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
                return render(request, 'verifica_codigo.html', {'form': form})
        else:
            return render(request, 'verifica_codigo.html', {'form': form})

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
    login_url = '/login/' # Redireciona se não estiver logado
    
    def post(self, request, produto_id):
        produto = Produto.objects.get(id=produto_id)
        
        # Pega ou cria um pedido "PENDENTE" para o usuário
        pedido, criado = Pedido.objects.get_or_create(
            usuario=request.user,
            situacao='PENDENTE'
        )
        
        # Adiciona o produto ao pedido
        pedido.produtos.add(produto)
        
        # Atualiza o total do pedido
        # Este é um jeito simples, para cenários mais complexos,
        # você pode querer usar um campo 'quantidade'
        total = pedido.produtos.aggregate(Sum('valor'))['valor__sum']
        pedido.total = total if total else 0
        pedido.save()

        return redirect('catalogo')

class VerPedidoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        try:
            pedido = Pedido.objects.get(usuario=request.user, situacao='PENDENTE')
        except Pedido.DoesNotExist:
            pedido = None
            
        return render(request, 'ver_pedido.html', {'pedido': pedido})

class FinalizarPedidoView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def post(self, request):
        try:
            pedido = Pedido.objects.get(usuario=request.user, situacao='PENDENTE')
            # Muda a situação para "FEITO" (ou o próximo passo do seu fluxo)
            pedido.situacao = 'FEITO'
            pedido.save()
            # Aqui você pode adicionar lógica de pagamento, etc.
        except Pedido.DoesNotExist:
            # Lidar com o caso de não haver pedido pendente
            pass
        return redirect('inicio') # Redireciona para a página inicial após finalizar

