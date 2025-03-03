from django.db import models
from currency.models import Currency
import uuid


# Create your models here.
class Country(models.Model):
   country_name = models.CharField(max_length=50)
   country_code = models.CharField(max_length=50)
   currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

   def __str__(self):
       return f"{self.country_name}"
   
class City(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city_name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")
    image=models.ImageField(upload_to='cities/',null=True,blank=True)

    def __str__(self):
        return f"{self.city_name}, {self.country.country_name}"