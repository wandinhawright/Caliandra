from urllib import request
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate , login
from .models import Usuario, Produto, Pedido
from .forms import LoginForm
# Create your views here.
class InicioView(View):
    def get(self, request):
        return render(request, 'inicio.html')

class LoginView(View):
    def logar ( self, request):
        if(request.method == 'POST'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            usuario = authenticate(request, username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('inicio')  # Redireciona para a página inicial após o login
            else:
                return render(request, 'login.html', {'error': 'Credenciais inválidas'})
        if(request.method == 'GET' and request.GET.get("action") == "registrar"):
            return render(request, 'registro.html')
        else:
            return render(request, 'login.html')

    form = LoginForm(request.GET or None)
    context={
        'form': form
    }

