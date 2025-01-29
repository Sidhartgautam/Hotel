from django.db import models

# Create your models here.
class Currency(models.Model):
    currency_name = models.CharField(max_length=50)
    currency_code = models.CharField(max_length=50)
    currency_symbol = models.CharField(max_length=50)

    def __str__(self):
         return f"{self.currency_name}"