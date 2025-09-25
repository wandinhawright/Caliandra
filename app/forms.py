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
        label="Nome completo"
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
        widget=forms.EmailInput(attrs={'placeholder': 'exemplo@dominio.com'})
    )
    telefone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '(99) 99999-9999'})
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

class CheckoutForm(forms.Form):
    # Informações de entrega
    endereco_entrega = forms.CharField(
        label="Endereço de Entrega",
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Rua, número, complemento'})
    )
    cidade = forms.CharField(
        label="Cidade",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Sua cidade'})
    )
    cep = forms.CharField(
        label="CEP",
        max_length=9,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '00000-000'})
    )
    
    # Informações adicionais
    observacoes = forms.CharField(
        label="Observações",
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Instruções especiais para entrega, observações sobre os produtos, etc.',
            'rows': 3
        })
    )
    
    # Confirmação
    termos_aceitos = forms.BooleanField(
        label="Li e aceito os termos de compra coletiva",
        required=True,
        error_messages={'required': 'Você deve aceitar os termos para continuar.'}
    )

    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep:
            # Remove caracteres não numéricos
            cep = ''.join(filter(str.isdigit, cep))
            if len(cep) != 8:
                raise forms.ValidationError('CEP deve ter 8 dígitos.')
            # Formatar CEP
            return f'{cep[:5]}-{cep[5:]}'
        return cep