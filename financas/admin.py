# financas/admin.py
from django.contrib import admin
# Importe TODOS os modelos que você quer ver no admin
from .models import Transacao, CartaoCredito, Categoria 

# Registre cada um deles
admin.site.register(Transacao)
admin.site.register(CartaoCredito)
admin.site.register(Categoria)