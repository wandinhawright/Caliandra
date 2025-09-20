from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=150,
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
    )

class RegistroForm(forms.Form):
    nome = forms.CharField(
        max_length=150,
        required=True,
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(),
        required=True,
    )
    confirmar_password = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(),
        required=True,
    )
    email = forms.EmailField(
        required=True,
    )
    telefone = forms.CharField(
        max_length=15,
        required=True,
    )
    endereco = forms.CharField(
        label="Endereço",
        max_length=255,
        required=True,
    )
class VerificationCodeForm(forms.Form):
    code = forms.CharField(
        label="Código de Verificação",
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '_ _ _ _ _ _'})
    )