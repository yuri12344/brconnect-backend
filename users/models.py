from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Telefone deve ser inserido no formato correto: '+554187941579'. Até 15 digitos."
)

class Company(models.Model):
    """
    A Company represents a company.
    """
    name            = models.CharField(max_length=255, verbose_name="Nome")
    address         = models.CharField(max_length=255, verbose_name="Endereço")
    phone           = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name="Numero de telefone") # validators should be a list
    description     = models.TextField(verbose_name="Descrição")
    owner           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies', verbose_name="Criador")
    date_created    = models.DateTimeField(auto_now_add=True, verbose_name="Data Criação")


    class Meta:
        db_table = 'companies'
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.name


class Customer(models.Model):
    """
    A Customer represents a customer.
    """
    name        = models.CharField(max_length=255, verbose_name="Name")
    email       = models.EmailField(max_length=255, null=True, blank=True, unique=True, verbose_name="Email")
    street      = models.CharField(max_length=255, null=True, blank=True, verbose_name="Street")
    state       = models.CharField(max_length=255, null=True, blank=True, verbose_name="State")
    city        = models.CharField(max_length=255, null=True, blank=True, verbose_name="City")
    zip         = models.CharField(max_length=255, null=True, blank=True, verbose_name="Zip Code")
    phone       = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name="Phone Number") # validators should be a list
    whatsapp    = models.CharField(max_length=20, null=True, blank=True, verbose_name="WhatsApp Number")
    birthday    = models.DateField(null=True, blank=True, verbose_name="Birthday")
    company     = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='customers', related_query_name='customer', verbose_name="Company"
    )
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Date Updated")

    class Meta:
        db_table = 'customers'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.name
