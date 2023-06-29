from django.core.validators import MinValueValidator
from simple_history.models import HistoricalRecords
from users.models import Company
from django.db import models


class Coupon(models.Model):
    """
    A Coupon represents a discount code that can be applied to products or categories.
    """
    code = models.CharField(max_length=255, unique=True, verbose_name="Codigo")
    description = models.TextField(null=True, blank=True, verbose_name="Descrição")
    category = models.ManyToManyField('Category', related_name='coupons', related_query_name='coupon', blank=True, verbose_name="Categoria")
    product = models.ManyToManyField('Product', related_name='coupons', related_query_name='coupon', blank=True, verbose_name="Produto")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='coupons', verbose_name="Empresa")

    class Meta:
        db_table = 'coupons'
        verbose_name = "Cupom"
        verbose_name_plural = "Cupons"

    def __str__(self):
        return self.code


class Category(models.Model):
    """
    A Category represents a group of products.
    """
    name = models.CharField(max_length=255, verbose_name="Nome")
    alias = models.CharField(max_length=255, verbose_name="Alias")
    description = models.TextField(null=True, blank=True, verbose_name="Descrição")
    products = models.ManyToManyField('Product', related_name='categories', related_query_name='category', blank=True, verbose_name="Produtos")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='categories', verbose_name="Empresa")
    affinity_categories = models.ManyToManyField('self', symmetrical=False, blank=True, verbose_name="Categorias de Afinidade")

    class Meta:
        db_table = 'categories'
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    A Product represents an item for sale.
    """
    name = models.CharField(max_length=255, verbose_name="Nome")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    description = models.TextField(null=True, blank=True, verbose_name="Descrição")
    active = models.BooleanField(default=True, verbose_name="Ativo")
    stock = models.IntegerField(validators=[MinValueValidator(0)], default=999, verbose_name="Estoque")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products', verbose_name="Empresa")
    history = HistoricalRecords(inherit=True)

    class Meta:
        db_table = 'products'
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """
    A ProductImage represents an image of a product.
    """
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name="Produto")
    url_secondary = models.URLField(verbose_name="URL Secundaria")
    image = models.ImageField(upload_to='products', null=True, blank=True, verbose_name="Imagem")
    description= models.CharField(max_length=255, verbose_name="Descrição")

    class Meta:
        db_table = 'images'
        verbose_name = "Imagem do Produto"
        verbose_name_plural = "Imagens do Produto"

    def __str__(self):
        return self.url



class Vitrine(models.Model):
    """
    A Vitrine represents a showcase of products.
    """
    name = models.CharField(max_length=255, verbose_name="Nome")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='vitrines', verbose_name="Categoria")
    products = models.ManyToManyField('Product', through='VitrineProduct', related_name='vitrines', related_query_name='vitrine', blank=True, verbose_name="Produtos")

    class Meta:
        db_table = 'vitrines'
        verbose_name = "Vitrine"
        verbose_name_plural = "Vitrines"

    def __str__(self):
        return self.name
    

class VitrineProduct(models.Model):
    """
    A VitrineProduct represents the relationship between a Vitrine and a Product.
    """
    vitrine = models.ForeignKey(Vitrine, on_delete=models.CASCADE, verbose_name="Vitrine")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produto")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Data adicionado")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Empresa")

    class Meta:
        db_table = 'vitrine_products'
        verbose_name = "Produto da Vitrine"
        verbose_name_plural = "Produtos da Vitrine"

    def __str__(self) -> str:
        return self.vitrine.name + ' - ' + self.product.name
