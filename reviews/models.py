import uuid
from django.db import models 
from property.models import Property
from users.models import User
from django.core.exceptions import ValidationError 


class PropertyReview(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property_reviewed = models.ForeignKey(Property, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.FloatField(null=True, blank=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def is_reply(self):
        return self.parent is not None

    def __str__(self):
        return f"Review by {self.user} on {self.property_reviewed}"

class GuestReview(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guest_reviews",null=True,blank=True)
    property = models.ForeignKey(Property, related_name='guest_reviews', on_delete=models.CASCADE)
    staff = models.FloatField()
    facilities = models.FloatField()
    cleanliness = models.FloatField()
    comfort = models.FloatField()
    value_for_money = models.FloatField()
    location = models.FloatField()
    free_wifi = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """
        Validates that all numerical fields have values less than 10.
        """
        fields_to_validate = [
            ('staff', self.staff),
            ('facilities', self.facilities),
            ('cleanliness', self.cleanliness),
            ('comfort', self.comfort),
            ('value_for_money', self.value_for_money),
            ('location', self.location),
            ('free_wifi', self.free_wifi)
        ]

        for field_name, value in fields_to_validate:
            if value >= 10:
                raise ValidationError({field_name: f"{field_name.replace('_', ' ').capitalize()} must be less than 10."})

    def save(self, *args, **kwargs):
        # Call the clean method to enforce validation before saving
        self.clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Guest Review for {self.property}"


