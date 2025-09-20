from urllib import request
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import Usuario, Produto, Pedido
from .forms import LoginForm , RegistroForm
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
            # Lógica para registro de novo usuário
            email = request.POST.get('email')
            password = request.POST.get('password')
            nome = request.POST.get('nome')
            telefone = request.POST.get('telefone')
            endereco = request.POST.get('endereco')

            # Verificar se usuário já existe
            if Usuario.objects.filter(email=email).exists():
                return render(request, 'registro.html', {
                    'form': RegistroForm(),
                    'error': 'Este email já está cadastrado.'
                })

            # Criar novo usuário
            try:
                usuario = Usuario(
                    email=email,
                    nome=nome,
                    telefone=telefone,
                    endereco=endereco
                )
                usuario.set_password(password)  # Criptografa a senha
                usuario.save()
                
                # Autenticar automaticamente o usuário após o registro
                login(request, usuario)
                return redirect('inicio')
            except Exception as e:
                return render(request, 'registro.html', {
                    'form': RegistroForm(),
                    'error': f'Erro ao criar usuário: {str(e)}'
                })

        else:
            # Lógica para login
            email = request.POST.get('email')
            password = request.POST.get('password')
            usuario = authenticate(request, email=email, password=password)

            if usuario is not None:
                login(request, usuario)
                return redirect('inicio')
            else:
                form = LoginForm()
                return render(request, 'login.html', {
                    'form': form,
                    'error': 'Credenciais inválidas'
                })


class LogoutView(View):
    def get(self, request):
        """Faz logout do usuário e redireciona para a página de login"""
        logout(request)
        return redirect('inicio')
    
    def post(self, request):
        """Permite logout via POST também"""
        logout(request)
        return redirect('inicio')

