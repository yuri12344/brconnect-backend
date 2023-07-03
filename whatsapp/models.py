from django.db import models
from users.models import Company

from abc import ABC

class WhatsAppSession(ABC):
    """
    A WhatsAppSession represents a WhatsApp Web session for a company.
    """
    name = models.CharField(max_length=255, verbose_name="Nome")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='whatsapp_sessions')
    phone_number = models.CharField(max_length=20, verbose_name="Número de Telefone")

    class Meta:
        abstract = True

    def __str__(self):
        return f'Sessão do WhatsApp para {self.company.name} ({self.phone_number})'


class WppConnectSession(WhatsAppSession):
    """
    A WppConnectSession represents a WppConnect WhatsApp Web session for a company.
    """
    session_token = models.CharField(max_length=255, verbose_name="Token da Sessão")
    session_name = models.CharField(max_length=255, verbose_name="Nome da Sessão")

    class Meta:
        db_table = 'wppconnect_sessions'
        verbose_name = "Sessão do WppConnect"
        verbose_name_plural = "Sessões do WppConnect"


class Campaign(models.Model):
    STATUS_CHOICE = (
        (0, 'Não enviado'),
        (1, 'Enviando'),
        (2, 'Enviado'),
        (3, 'Erro'),
    )
    SCHEDULE_TYPE_CHOICES = (
        ('now', 'Enviar Agora'),
        ('scheduled', 'Agendar Envio'),
        ('daily', 'Enviar Diariamente'),
        ('weekly', 'Enviar Semanalmente'),
        ('monthly', 'Enviar Mensalmente'),
    )

    name = models.CharField(max_length=200, verbose_name="Nome")
    description = models.TextField(verbose_name="Descrição")
    status = models.IntegerField(choices=STATUS_CHOICE, default=0, verbose_name="Status")
    schedule_type = models.CharField(max_length=10, choices=SCHEDULE_TYPE_CHOICES, default='now')
    schedule_time = models.TimeField(null=True, blank=True)
    schedule_day = models.IntegerField(null=True, blank=True)


class TextMessage(models.Model):
    message = models.TextField(verbose_name="Mensagem")
    class Meta:
        verbose_name = "Texto"
        verbose_name_plural = "Textos"
    def __str__(self):
        return self.message


class ImageMessage(models.Model):
    name    = models.CharField(max_length=200, verbose_name="Nome")
    image   = models.ImageField(upload_to='images/', verbose_name="Imagem")
    caption = models.CharField(max_length=200, verbose_name="Legenda")
    class Meta:
        verbose_name = "Imagem"
        verbose_name_plural = "Imagens"
    def __str__(self):
        return self.image.url