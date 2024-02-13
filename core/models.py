from django.db import models

class BaseModel(models.Model):
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE, verbose_name="Empresa")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        
