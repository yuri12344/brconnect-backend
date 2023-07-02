from django.db import models
from users.models import Company

class WhatsAppSession(models.Model):
    """
    A WhatsAppSession represents a WhatsApp Web session for a company.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='whatsapp_sessions')
    session_token = models.CharField(max_length=255, verbose_name="Token da Sessão")
    phone_number = models.CharField(max_length=20, verbose_name="Número de Telefone")
    name = models.CharField(max_length=255, verbose_name="Nome")

    class Meta:
        db_table = 'whatsapp_sessions'
        verbose_name = "Sessão do WhatsApp"
        verbose_name_plural = "Sessões do WhatsApp"

    def __str__(self):
        return f'Sessão do WhatsApp para {self.company.name} ({self.phone_number})'


class Campanha(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome")
    description = models.TextField(verbose_name="Descrição")
    start_date = models.DateTimeField(verbose_name="Data de início")
    end_date = models.DateTimeField(verbose_name="Data de término")
    status = models.BooleanField(default=False, verbose_name="Enviado")


class TextMessage(models.Model):
    message = models.TextField(verbose_name="Mensagem")

    class Meta:
        verbose_name = "Texto"
        verbose_name_plural = "Textos"

    def __str__(self):
        return self.message


class ImageMessage(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome")
    image = models.ImageField(upload_to='images/', verbose_name="Imagem")
    caption = models.CharField(max_length=200, verbose_name="Legenda")

    class Meta:
        verbose_name = "Imagem"
        verbose_name_plural = "Imagens"

    def __str__(self):
        return self.image.url