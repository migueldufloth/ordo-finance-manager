from django.contrib import admin
from django.urls import path, include
from financas import views as financas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('transacoes/', include('financas.urls')),
    path('', financas_views.dashboard, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
]
