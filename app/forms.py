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
        max_length=255,
        required=True,
    )