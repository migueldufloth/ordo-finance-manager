from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    """Armazena as categorias das transações do usuário"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    class Meta:
        """Define as configurações do modelo Categoria"""
        unique_together = ('usuario', 'nome')
        verbose_name_plural = "Categorias"

    def __str__(self):
        """Retorna o nome da categoria como representação em string"""
        return self.nome


class CartaoCredito(models.Model):
    """Modela as informações de um cartão de crédito"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, verbose_name="Nome do Cartão")
    limite = models.DecimalField(max_digits=10, decimal_places=2)
    dia_fechamento = models.IntegerField(verbose_name="Dia do Fechamento")
    dia_vencimento = models.IntegerField(verbose_name="Dia do Vencimento")
    COR_CHOICES = [
        ("BLUE", "Azul"),
        ("GREEN", "Verde"),
        ("RED", "Vermelho"),
        ("PURPLE", "Roxo"),
        ("BLACK", "Preto"),
        ("ORANGE", "Laranja"),
        ("GRAY", "Cinza"),
    ]
    cor = models.CharField(max_length=6, choices=COR_CHOICES, default="GRAY", verbose_name="Cor do Cartão")

    class Meta:
        """Define as configurações do modelo CartaoCredito"""
        verbose_name = "Cartão de Crédito"
        verbose_name_plural = "Cartões de Crédito"

    def __str__(self):
        """Retorna o nome do cartão como representação em string"""
        return self.nome


class Transacao(models.Model):
    """Registra as transações financeiras de receita ou despesa"""
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Usuário")
    data = models.DateField()
    TIPO_CHOICES = [
        ("RECEITA", "Receita"),
        ("DESPESA", "Despesa"),
    ]
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)

    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    cartao_credito = models.ForeignKey(
        CartaoCredito, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Cartão de Crédito")
    fatura_paga = models.BooleanField(
        default=False, verbose_name="Fatura Paga")

    class Meta:
        """Define as configurações do modelo Transacao"""
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ['-data']

    def __str__(self):
        """Retorna uma representação em string formatada da transação"""
        return f"[{self.data}] {self.descricao} - R$ {self.valor}"
    





































    