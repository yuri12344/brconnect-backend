from django.db import models

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