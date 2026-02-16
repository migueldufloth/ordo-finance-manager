# financas/forms.py
from django import forms
from .models import Transacao, Categoria, CartaoCredito

class TransacaoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.none(),
        required=True,
        empty_label="-- Selecione uma Categoria --", 
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'})
    )
    cartao_credito = forms.ModelChoiceField(
        queryset=CartaoCredito.objects.none(),
        required=False,
        empty_label="-- Nenhum --",
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'})
    )

    class Meta:
        model = Transacao
        fields = ['data', 'tipo', 'descricao', 'valor', 'categoria', 'cartao_credito']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}),
            'descricao': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Ex: Salário, Aluguel'}),
            'valor': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        if user:
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=user)
            self.fields['cartao_credito'].queryset = CartaoCredito.objects.filter(usuario=user)
            
class CartaoCreditoForm(forms.ModelForm):
    class Meta:
        model = CartaoCredito
        fields = ['nome', 'cor', 'limite', 'dia_fechamento', 'dia_vencimento']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'placeholder': 'Ex: Nubank Platinum'}),
            'cor': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg'}),
            'limite': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'step': '0.01'}),
            'dia_fechamento': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'min': '1', 'max': '31'}),
            'dia_vencimento': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'min': '1', 'max': '31'}),
        }