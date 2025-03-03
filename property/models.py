from django.db import models
from ckeditor.fields import RichTextField
from country.models import Country,City
from currency.models import Currency
from users.models import User
import uuid
from core.utils.slugify import unique_slug_generator
# Create your models here.

class PropertyCategory(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=50)
    description=RichTextField(null=True,blank=True)
    image=models.ImageField(upload_to='category/',null=True,blank=True)

    def __str__(self):
        return f"{self.category_name}"
    
class Property(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property_name = models.CharField(max_length=50)
    is_single_unit = models.BooleanField(
        default=False,
        help_text="Indicates if this property is booked as a single unit (e.g., cottage or villa).",
        null=True,
        blank=True
    )
    address = models.CharField(max_length=50)
    description = models.TextField()
    star_rating_property=models.IntegerField(default=0,null=True,blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    currency=models.ForeignKey(Currency, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    city=models.ForeignKey(City, on_delete=models.CASCADE, related_name="properties",null=True,blank=True)
    state = models.CharField(max_length=50)
    lng = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    lat = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(PropertyCategory, on_delete=models.CASCADE, related_name="properties")
    language=models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = unique_slug_generator(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.property_name}"
    
class BreakfastInfo(models.Model):
    property=models.ForeignKey(Property, on_delete=models.CASCADE, related_name="breakfast_info")
    serve_breakfast=models.BooleanField(default=False)
    breakfast_included = models.BooleanField(default=False) 
    breakfast_type = models.JSONField(
        default=list,
        blank=True,
        null=True,
        help_text="List of breakfast types served (e.g., ['continental', 'vegan'])"
    )
    extra_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Extra cost for breakfast if not included"
    )

    def save(self, *args, **kwargs):
        if self.breakfast_included:
            self.extra_cost = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Breakfast Info (Serve: {self.serve_breakfast}, Included: {self.breakfast_included})"
    
class ParkingInfo(models.Model):
    """
    Model to store parking details for a property.
    """
    PARKING_CHOICES = [
        ('free', 'Free'),
        ('paid', 'Paid'),
        ('not_available', 'Not Available'),
    ]

    PARKING_LOCATION_CHOICES = [
        ('onsite', 'Onsite'),
        ('offsite', 'Offsite'),
    ]

    PARKING_ACCESS_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name="parking_info",null=True,blank=True)
    parking_availability = models.CharField(
        max_length=20,
        choices=PARKING_CHOICES,
        default='not_available',
        help_text="Indicates if parking is free, paid, or not available"
    )
    parking_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Price for parking if it is paid"
    )
    reservation_required = models.BooleanField(
        default=False,
        help_text="Indicates if a reservation is required for parking"
    )
    parking_location = models.CharField(
        max_length=20,
        choices=PARKING_LOCATION_CHOICES,
        blank=True,
        null=True,
        help_text="Indicates if parking is onsite or offsite"
    )
    parking_access = models.CharField(
        max_length=20,
        choices=PARKING_ACCESS_CHOICES,
        blank=True,
        null=True,
        help_text="Indicates if parking is private or public"
    )

    def save(self, *args, **kwargs):
        # Ensure parking_price is set only when parking_availability is 'paid'
        if self.parking_availability != 'paid':
            self.parking_price = None
        super().save(*args, **kwargs)

    def __str__(self):
        if self.parking_availability == 'not_available':
            return "Parking Not Available"
        return f"Parking: {self.parking_availability.capitalize()}"


    
class PropertyImage(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image=models.ImageField(upload_to='property/',null=True,blank=True)
    property=models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return f"{self.property.property_name}"
    
class Amenity(models.Model):
    """
    Represents an amenity, such as Free Wi-Fi, Parking, Pool, etc.
    """
    name = models.CharField(max_length=100, unique=True)  # e.g., "Free Wi-Fi", "Swimming Pool"
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return self.name


class PropertyAmenities(models.Model):
    """
    Represents the many-to-many relationship between properties and amenities.
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="amenities")
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE, related_name="properties")
    is_available = models.BooleanField(default=True)  # Availability of the amenity

    def __str__(self):
        return f"{self.amenity.name} at {self.property.property_name}"
    
class Policy(models.Model):
    property=models.ForeignKey(Property, on_delete=models.CASCADE, related_name="policies")
    
    # Check-in and Check-out times
    checkin_time_from = models.TimeField(
        help_text="Time when check-in starts (e.g., 14:00).", 
        blank=True, null=True
    )
    checkin_time_to = models.TimeField(
        help_text="Time when check-in ends (e.g., 23:59).", 
        blank=True, null=True
    )

    # ✅ Store Check-out Time as a Range
    checkout_time_from = models.TimeField(
        help_text="Time when check-out starts (e.g., 06:00).", 
        blank=True, null=True
    )
    checkout_time_to = models.TimeField(
        help_text="Time by which guests must check out (e.g., 12:00).", 
        blank=True, null=True
    )

    # Children Policy
    children_allowed = models.BooleanField(default=True, help_text="Are children allowed?")
    extra_beds_available = models.BooleanField(default=False, help_text="Are extra beds available for children?")
    extra_bed_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="Cost of an extra bed if available."
    )

    # Pet Policy
    pets_allowed = models.BooleanField(default=False, help_text="Are pets allowed?")
    pet_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="Fee for bringing pets, if applicable."
    )
    pet_details = models.TextField(
        blank=True, 
        null=True, 
        help_text="Additional details about the pet policy (e.g., allowed pet types or size limits)."
    )

    def save(self, *args, **kwargs):
        # Ensure extra_bed_cost is set only when extra_beds_available is True
        if not self.extra_beds_available:
            self.extra_bed_cost = None

        # Ensure pet_fee is set only when pets_allowed is True
        if not self.pets_allowed:
            self.pet_fee = None
            self.pet_details = None
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Policy for {self.property.property_name}"
    

class CancellationPolicy(models.Model):
    CANCELLATION_FEE_TYPE_CHOICES = [
        ('percentage', 'Percentage of Total Price'),
        ('fixed', 'Fixed Amount'),
        ('none', 'No Fee'),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="cancellation_policy",
        help_text="The property this cancellation policy belongs to."
    )
    cancellations_allowed = models.BooleanField(
        default=True,
        help_text="Indicates if cancellations are allowed for this property."
    )
    cancellation_deadline_days = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
        help_text="Number of days before check-in when cancellations are allowed (0 means any time)."
    )
    cancellation_fee_type = models.CharField(
        max_length=20,
        choices=CANCELLATION_FEE_TYPE_CHOICES,
        default='none',
        help_text="Type of cancellation fee (percentage, fixed, or none)."
    )
    cancellation_fee_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Amount of the cancellation fee (either percentage or fixed)."
    )
    refundable = models.BooleanField(
        default=True,
        help_text="Indicates if the booking amount is refundable after cancellation."
    )
    additional_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes or terms regarding the cancellation policy."
    )

    def save(self, *args, **kwargs):
        """
        Validate the cancellation fee type and amount.
        """
        if self.cancellation_fee_type == 'none':
            self.cancellation_fee_amount = None
        elif self.cancellation_fee_type == 'percentage' and self.cancellation_fee_amount:
            if self.cancellation_fee_amount > 100 or self.cancellation_fee_amount < 0:
                raise ValueError("Percentage fee must be between 0 and 100.")
        elif self.cancellation_fee_type == 'fixed' and self.cancellation_fee_amount < 0:
            raise ValueError("Fixed cancellation fee must be non-negative.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cancellation Policy for {self.property.property_name}"
    
class SingleUnitPrice(models.Model):
    property = models.OneToOneField(
        Property, 
        on_delete=models.CASCADE, 
        related_name='single_unit_price'
    )
    base_price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    seasonal_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_percentage = models.FloatField(default=0)
    currency=models.ForeignKey(Currency, on_delete=models.CASCADE,blank=True, null=True)

    def get_effective_price(self):
        price = self.seasonal_price if self.seasonal_price else self.base_price_per_night
        if self.discount_percentage > 0:
            price -= price * (self.discount_percentage / 100)
        return round(price, 2)

    def save(self, *args, **kwargs):
        if self.base_price_per_night is None:
            raise ValueError("Base price per night is required.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Single Unit Price for {self.property.property_name}"
