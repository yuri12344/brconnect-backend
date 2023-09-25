from django.core.validators import RegexValidator
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from core.models import BaseModel
from core.services.services import STATE_CHOICES, INDUSTRY_CHOICES, EMPLOYEE_COUNT_CHOICES

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Telefone deve ser inserido no formato correto: '+554187941579'. Até 15 digitos."
)

class Company(models.Model):
    name                    = models.CharField(max_length=255, verbose_name="Nome", blank=True, null=True)
    street                  = models.CharField(max_length=255, verbose_name="Rua", blank=True, null=True)
    city                    = models.CharField(max_length=255, verbose_name="Cidade", blank=True, null=True)
    state                   = models.CharField(max_length=2, choices=STATE_CHOICES, null=True, blank=True, verbose_name="Estado")
    zip_code                = models.CharField(max_length=255, verbose_name="CEP", blank=True, null=True)
    phone                   = models.CharField(max_length=17, blank=True, null=True, verbose_name="Numero de telefone")
    email                   = models.EmailField(max_length=255, verbose_name="Email", blank=True, null=True)
    website                 = models.URLField(max_length=255, null=True, blank=True, verbose_name="Website")
    description             = models.TextField(verbose_name="Descrição", blank=True, null=True)
    owner                   = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company', verbose_name="Criador")
    chave_pix               = models.CharField(max_length=255, verbose_name="Chave Pix", blank=True, null=True)
    date_updated            = models.DateTimeField(auto_now=True, verbose_name="Data Atualização")
    cnpj                    = models.CharField(max_length=255, verbose_name="CNPJ", blank=True, null=True)
    logo                    = models.ImageField(upload_to='logos/', null=True, blank=True, verbose_name="Logo")
    industry                = models.CharField(max_length=255, choices=INDUSTRY_CHOICES, blank=True, null=True, verbose_name="Indústria")
    order_expiration_days   = models.PositiveIntegerField(default=7, verbose_name="Dias para expiração do pedido não pago e não enviado")
    employee_count          = models.IntegerField(choices=EMPLOYEE_COUNT_CHOICES, blank=True, null=True, verbose_name="Quantidade de Funcionários")
    whatsapp_service        = models.CharField(max_length=255, choices=[('wppconnect', 'WppConnect'), ('baileys', 'Baileys')], default='wppconnect')

    class Meta:
        db_table = 'companies'
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.name
    
class Region(BaseModel):
    regiao  = models.CharField(max_length=255, verbose_name="Regiao")
    cost    = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Custo frete')
 
    class Meta:
        db_table = 'regions'
        verbose_name = "Região"
        verbose_name_plural = "Regiões"

    def __str__(self):
        return self.regiao

class Customer(BaseModel):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    name                = models.CharField(max_length=255, verbose_name="Name")
    whatsapp            = models.CharField(max_length=20, null=True, blank=True, verbose_name="WhatsApp")
    street              = models.CharField(max_length=255, null=True, blank=True, verbose_name="Logradouro")
    number              = models.CharField(max_length=255, null=True, blank=True, verbose_name="Número")
    complement          = models.CharField(max_length=255, null=True, blank=True, verbose_name="Complemento")
    neighborhood        = models.CharField(max_length=255, null=True, blank=True, verbose_name="Bairro")
    zip                 = models.CharField(max_length=255, null=True, blank=True, verbose_name="CEP")
    city                = models.CharField(max_length=255, null=True, blank=True, verbose_name="Cidade")
    state               = models.CharField(max_length=2, choices=STATE_CHOICES, null=True, blank=True, verbose_name="Estado")
    region              = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Regiao")
    email               = models.EmailField(max_length=255, null=True, blank=True, verbose_name="Email")    
    birthday            = models.DateField(null=True, blank=True, verbose_name="Birthday")
    score               = models.IntegerField(default=0, verbose_name="Score")
    age                 = models.IntegerField(null=True, blank=True, verbose_name="Idade")
    gender              = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True, verbose_name="Gênero")
    interaction_history = models.TextField(null=True, blank=True, verbose_name="Histórico de Interações")
    favorite_product    = models.ForeignKey(
        'products.Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='loved_by', verbose_name="Produto Favorito"
    )
    purchase_history    = models.ManyToManyField(
        'sales.Order', related_name='purchasing_customers', blank=True, verbose_name="Histórico de Pedidos"
    )
    preferences = models.ManyToManyField('products.Product', blank=True, verbose_name="Preferências de Produto")

    class Meta:
        db_table = 'customers'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        unique_together = ('whatsapp', 'company',)

    def __str__(self):
        return self.name
    
    def has_order(self) -> bool:
        """
        Verifica se o cliente possui alguma ordem que está paga e não expirada.

        Retorna:
            bool: True se existe pelo menos uma ordem paga e não expirada, caso contrário False.
        """
        orders = self.orders.all()
        for order in orders:
            if not order.is_paid() and not order.is_expired():
                return True
        return False
    
    def get_address(self):
        address_parts = [
            self.street,
            self.number,
            self.complement,
            self.neighborhood,
            self.zip,
            self.city,
            self.state,
        ]
        return ', '.join(filter(None, address_parts))
    
    def has_address(self):
        return bool(self.street and self.state and self.city and self.zip)

    def calculate_score(self):
        self.score = self.interactions.aggregate(total_score=models.Sum('score'))['total_score'] or 0
        self.save()
    
    @property
    def interaction_history(self):
        return "\n".join(interaction.description for interaction in self.interactions.all())
    
class CustomerGroup(BaseModel):
    """
    A CustomerGroup represents a group of customers.
    """
    name        = models.CharField(max_length=50, verbose_name="Nome do Grupo")
    customers   = models.ManyToManyField(Customer, related_name='groups', blank=True, verbose_name="Clientes")

    class Meta:
        db_table = 'customer_groups'
        verbose_name = "Grupos de cliente"
        verbose_name_plural = "Grupos de clientes"

    def __str__(self):
        return self.name


class Interaction(BaseModel):
    name        = models.CharField(max_length=255, verbose_name="Nome", default="Interação")
    description = models.TextField(verbose_name="Descrição", blank=True, null=True)
    date        = models.DateTimeField(auto_now_add=True, verbose_name="Data da Interação")
    score       = models.IntegerField(verbose_name="Pontuação", default=5)
    customers   = models.ManyToManyField(Customer, related_name='interactions', verbose_name="Clientes", blank=True)

    class Meta:
        db_table = 'interactions'
        verbose_name = "Interação"
        verbose_name_plural = "Interações"

    def __str__(self):
        return f'Interação {self.name}'


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
