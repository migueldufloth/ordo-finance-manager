from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from .models import Transacao, CartaoCredito
from .forms import TransacaoForm, CartaoCreditoForm


@login_required
def dashboard(request):
    """Exibe o painel principal com um resumo das finanças do usuário"""

    transacoes = Transacao.objects.filter(usuario=request.user)
    total_receitas = (
        transacoes.filter(tipo="RECEITA").aggregate(Sum("valor"))["valor__sum"] or 0
    )
    total_despesas = (
        transacoes.filter(tipo="DESPESA").aggregate(Sum("valor"))["valor__sum"] or 0
    )
    saldo_total = total_receitas - total_despesas

    ano_atual = datetime.now().year
    mes_atual = datetime.now().month
    receitas_mes = (
        transacoes.filter(
            tipo="RECEITA", data__year=ano_atual, data__month=mes_atual
        ).aggregate(Sum("valor"))["valor__sum"]
        or 0
    )
    despesas_mes = (
        transacoes.filter(
            tipo="DESPESA", data__year=ano_atual, data__month=mes_atual
        ).aggregate(Sum("valor"))["valor__sum"]
        or 0
    )
    ultimos_lancamentos = transacoes.order_by("-data")[:5]

    contexto = {
        "saldo_total": saldo_total,
        "receitas_mes": receitas_mes,
        "despesas_mes": despesas_mes,
        "ultimos_lancamentos": ultimos_lancamentos,
    }
    return render(request, "financas/dashboard.html", contexto)


@login_required
def lista_transacoes(request):
    """Lista todas as transações do usuário logado"""

    transacoes = Transacao.objects.filter(usuario=request.user)
    return render(request, "financas/lista_transacoes.html", {"transacoes": transacoes})


@login_required
def adicionar_transacao(request):
    """Processa o formulário para adicionar uma nova transação"""

    if request.method == "POST":
        form = TransacaoForm(request.POST, user=request.user)
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.usuario = request.user
            transacao.save()
            return redirect("lista_transacoes")
    else:
        form = TransacaoForm(user=request.user)

    return render(request, "financas/adicionar_transacao.html", {"form": form})


@login_required
def remover_transacao(request, pk):
    """Remove uma transação existente"""
    transacao = get_object_or_404(Transacao, pk=pk, usuario=request.user)
    
    if request.method == "POST":
        transacao.delete()
        return redirect("lista_transacoes")
        
    return render(request, "financas/confirm_delete.html", {"object": transacao, "type": "transação"})


class CartaoCreditoListView(LoginRequiredMixin, ListView):
    """Exibe a lista de cartões de crédito do usuário"""

    model = CartaoCredito
    template_name = "financas/cartao_credito_list.html"

    def get_queryset(self):
        return CartaoCredito.objects.filter(usuario=self.request.user)


class CartaoCreditoCreateView(LoginRequiredMixin, CreateView):
    """Permite que o usuário adicione um novo cartão de crédito"""

    model = CartaoCredito
    form_class = CartaoCreditoForm
    template_name = "financas/cartao_credito_form.html"
    success_url = reverse_lazy("cartao_credito_list")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class CartaoCreditoUpdateView(LoginRequiredMixin, UpdateView):
    """Permite que o usuário edite um cartão de crédito existente"""

    model = CartaoCredito
    form_class = CartaoCreditoForm
    template_name = "financas/cartao_credito_form.html"
    success_url = reverse_lazy("cartao_credito_list")

    def get_queryset(self):
        return CartaoCredito.objects.filter(usuario=self.request.user)


class CartaoCreditoDeleteView(LoginRequiredMixin, DeleteView):
    """Permite que o usuário remova um cartão de crédito"""
    model = CartaoCredito
    template_name = "financas/confirm_delete.html"
    success_url = reverse_lazy("cartao_credito_list")

    def get_queryset(self):
        return CartaoCredito.objects.filter(usuario=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'cartão de crédito'
        return context
