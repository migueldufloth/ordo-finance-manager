from django.urls import path
from .views import (
    lista_transacoes,
    adicionar_transacao,
    CartaoCreditoListView,
    CartaoCreditoCreateView,
    CartaoCreditoUpdateView,
    CartaoCreditoDeleteView,
    remover_transacao,
)

urlpatterns = [
    # Rotas para transações
    path('', lista_transacoes, name='lista_transacoes'),
    path('adicionar/', adicionar_transacao, name='adicionar_transacao'),
    path('<int:pk>/remover/', remover_transacao, name='remover_transacao'),

    # Rotas para cartões de crédito
    path('cartoes/', CartaoCreditoListView.as_view(), name='cartao_credito_list'),
    path('cartoes/adicionar/', CartaoCreditoCreateView.as_view(), name='cartao_credito_create'),
    path('cartoes/<int:pk>/editar/', CartaoCreditoUpdateView.as_view(), name='cartao_credito_update'),
    path('cartoes/<int:pk>/remover/', CartaoCreditoDeleteView.as_view(), name='cartao_credito_delete'),
]