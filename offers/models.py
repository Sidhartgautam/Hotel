from django.db import models
from property.models import Property
from datetime import date, timedelta

class WeeklyOffer(models.Model):
    property = models.ForeignKey(
        Property, 
        on_delete=models.CASCADE, 
        related_name="weekly_offers"
    )
    discount_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="Discount percentage for the offer."
    )
    start_date = models.DateField(help_text="Start date of the weekly offer.")
    end_date = models.DateField(help_text="End date of the weekly offer.")
    description = models.TextField(blank=True, null=True, help_text="Details about the offer.")

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__lte=models.F('end_date')),
                name="valid_offer_date_range"
            )
        ]

    def is_active(self):
        today = date.today()
        return self.start_date <= today <= self.end_date

    def __str__(self):
        return f"Weekly Offer for {self.property.property_name} ({self.discount_percentage}% off)"
