from django.core.validators import MinValueValidator
from simple_history.models import HistoricalRecords
from users.models import Company
from django.db import models
from datetime import datetime, timedelta

def get_expiration_date():
    return datetime.now() + timedelta(days=7)

class Category(models.Model):
    """
    A Category represents a group of products.
    """
    name                = models.CharField(max_length=255, verbose_name="Nome")
    alias               = models.CharField(max_length=255, verbose_name="Alias")
    description         = models.TextField(null=True, blank=True, verbose_name="Descrição")
    products            = models.ManyToManyField('Product', related_name='categories', related_query_name='category', blank=True, verbose_name="Produtos")
    company             = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='categories', verbose_name="Empresa")
    featured_products   = models.ManyToManyField('Product', related_name='featured_categories', related_query_name='featured_category', blank=True, verbose_name="Produtos Destaque")

    class Meta:
        db_table = 'categories'
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return f'{self.alias} - {self.name}'

class CategoryAffinity(models.Model):
    """
    A CategoryAffinity represents an affinity relationship between two categories.
    """
    category1           = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='affinities_as_category1')
    category2           = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='affinities_as_category2')
    image               = models.ImageField(upload_to='affinity_images/', null=True, blank=True)
    company             = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='category_affinities', verbose_name="Empresa")
    text_recomendation  = models.TextField(null=True, blank=True, verbose_name="Texto de Recomendação")

    class Meta:
        unique_together = ('category1', 'category2')  # Each pair of categories should have at most one affinity

    def __str__(self):
        return f'Affinity from {self.category1.name} to {self.category2.name}'

class Product(models.Model):
    """
    A Product represents an item for sale.
    """
    name            = models.CharField(max_length=255, verbose_name="Nome")
    price           = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço", default=0.00)
    description     = models.TextField(null=True, blank=True, verbose_name="Descrição")
    active          = models.BooleanField(default=True, verbose_name="Ativo")
    stock           = models.IntegerField(validators=[MinValueValidator(0)], default=999, verbose_name="Estoque")
    company         = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products', verbose_name="Empresa")
    retailer_id     = models.CharField(max_length=255, verbose_name="Código do item", null=True, blank=True)
    history         = HistoricalRecords(inherit=True)

    class Meta:
        db_table = 'products'
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        categories = self.categories.all()
        if categories:
            categories_name = ""
            for categorie in categories:
                categories_name += categorie.name + ", "

            return f'id: {self.pk} | Produto: {self.name} | Categoria: {categories_name}'
        else:
            return f'id: {self.pk} | Produto: {self.name}'

class ProductImage(models.Model):
    """
    A ProductImage represents an image of a product.
    """
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name="Produto")
    url_secondary = models.URLField(verbose_name="URL Secundaria", null=True, blank=True)
    image = models.ImageField(upload_to='products', null=True, blank=True, verbose_name="Imagem")
    description= models.CharField(max_length=255, verbose_name="Descrição", null=True, blank=True)

    class Meta:
        db_table = 'images'
        verbose_name = "Imagem do Produto"
        verbose_name_plural = "Imagens do Produto"

    def __str__(self):
        return f'Image from: {self.product.name}'

class WhatsAppProductInfo(models.Model):
    """
    A WhatsAppProductInfo represents specific information related to a product on WhatsApp.
    """
    id = models.CharField(max_length=255, verbose_name="ID produto Meta", primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Nome do Produto no WhatsApp", null=True, blank=True)
    description = models.TextField(verbose_name="Descrição do Produto no WhatsApp", null=True, blank=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='whatsapp_info')
    link = models.URLField(verbose_name="Link no Whatsapp", null=True, blank=True)
    images = models.ManyToManyField(ProductImage, blank=True, related_name='whatsapp_products')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='whatsapp_products', verbose_name="Empresa")

    class Meta:
        db_table = 'whatsapp_product_info'
        verbose_name = "Produto no WhatsApp"
        verbose_name_plural = "Produtos no WhatsApp"

    def __str__(self):
        return f'{self.product.name} | ID Produto pai: {self.product.id}'