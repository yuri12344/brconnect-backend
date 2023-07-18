from users.models import BaseModel
from django.db import models


class Category(BaseModel):
    name                = models.CharField(max_length=255, verbose_name="Nome")
    alias               = models.CharField(max_length=255, verbose_name="Alias")
    description         = models.TextField(null=True, blank=True, verbose_name="Descrição")
    products            = models.ManyToManyField("Product", related_name="categories", related_query_name="category", blank=True, verbose_name="Produtos")

    class Meta:
        db_table            = "categories"
        verbose_name        = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return f"{self.alias} - {self.name}"

class CategoryRecommendation(BaseModel):
    category_a              = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recommendations_as_category_a", verbose_name="Categoria A")
    category_b              = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recommendations_as_category_b", verbose_name="Categoria B")
    recommendation_text     = models.TextField(
        null=False, blank=False, verbose_name="Texto de Recomendação", 
        help_text="Mensagem de recomendação enviada ao cliente, sugerindo um produto da categoria B, caso o carrinho não contenha produtos dessa categoria."
    )
    recommendation_image    = models.ImageField(upload_to="category_recomendations_images/", null=True, blank=True)

    class Meta:
        verbose_name = "Recomendação por categoria"
        
    def __str__(self):
        return f"Recomendação da categoria: {self.category_a.name} para a categoria: {self.category_b.name}"

class Product(BaseModel):
    name                = models.CharField(max_length=255, verbose_name="Nome")
    price               = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço", default=0.00)
    description         = models.TextField(null=True, blank=True, verbose_name="Descrição")
    retailer_id         = models.CharField(max_length=255, verbose_name="Código do item", null=True, blank=True)
    whatsapp_meta_id    = models.CharField(max_length=255, verbose_name="ID produto Meta", null=True, blank=True)
    whatsapp_link       = models.URLField(verbose_name="Link no Whatsapp", null=True, blank=True)

    class Meta:
        db_table = "products"
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return f"id: {self.pk} | Produto: {self.name}"


class ProductImage(BaseModel):
    product         = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE, verbose_name="Produto")
    url_secondary   = models.URLField(verbose_name="URL Secundaria", null=True, blank=True)
    image           = models.ImageField(upload_to="products", null=True, blank=True, verbose_name="Imagem")
    description     = models.CharField(max_length=255, verbose_name="Descrição", null=True, blank=True)

    class Meta:
        db_table            = "images"
        verbose_name        = "Imagem do Produto"
        verbose_name_plural = "Imagens do Produto"

    def __str__(self):
        return f"Image from: {self.product.name}"
