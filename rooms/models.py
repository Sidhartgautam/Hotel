from django.db import models
import uuid
from currency.models import Currency
from datetime import datetime,date

# Create your models here.
class BedType(models.Model):
    """
    Model to define bed types.
    """
    BED_TYPE_CHOICES = [
        ('single_bed', 'Single Bed'),
        ('double_bed', 'Double Bed'),
        ('queen_bed', 'Queen Bed'),
        ('king_bed', 'King Bed'),
        ('sofa_bed', 'Sofa Bed'),
        ('bunk_bed', 'Bunk Bed'),
        ('futon', 'Futon'),
        ('crib', 'Crib'),
        ('twin_beds', 'Twin Beds'),
        ('triple_beds', 'Triple Beds'),
        ('quad_beds', 'Quad Beds'),
        ('octuple_beds', 'Octuple Beds'),
        ('full_beds', 'Full Beds'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bed_type = models.CharField(max_length=50, choices=BED_TYPE_CHOICES, unique=True)

    def __str__(self):
        return self.get_bed_type_display()
    
class RoomAmenities(models.Model):
    """
    Amenities specific to individual rooms.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_type = models.ForeignKey(
        'RoomType',
        on_delete=models.CASCADE,
        related_name='all_room_amenities',  # Unique related name
        help_text="Room type that these amenities belong to",
        null=True,
        blank=True
    )
    # General Room Amenities
    air_conditioning = models.BooleanField(default=False)
    free_wifi = models.BooleanField(default=False)
    television = models.BooleanField(default=False)
    minibar = models.BooleanField(default=False)
    wardrobe = models.BooleanField(default=False)
    desk = models.BooleanField(default=False)
    telephone = models.BooleanField(default=False)
    safe = models.BooleanField(default=False)
    soundproofing = models.BooleanField(default=False)
    ironing_facilities = models.BooleanField(default=False)

    # Bed-related Amenities
    extra_long_beds = models.BooleanField(default=False)  # Beds > 6.5 ft
    electric_blankets = models.BooleanField(default=False)

    # View-related Amenities
    garden_view = models.BooleanField(default=False)
    city_view = models.BooleanField(default=False)
    mountain_view = models.BooleanField(default=False)
    landmark_view = models.BooleanField(default=False)
    pool_view = models.BooleanField(default=False)

    # Bathroom Amenities
    attached_bathroom = models.BooleanField(default=False)
    free_toiletries = models.BooleanField(default=False)
    shower = models.BooleanField(default=False)
    bathtub = models.BooleanField(default=False)
    bidet = models.BooleanField(default=False)
    hairdryer = models.BooleanField(default=False)
    slippers = models.BooleanField(default=False)
    towels = models.BooleanField(default=False)
    toilet = models.BooleanField(default=False)

    # Room Features
    balcony = models.BooleanField(default=False)
    patio = models.BooleanField(default=False)
    terrace = models.BooleanField(default=False)
    private_entrance = models.BooleanField(default=False)
    kitchenette = models.BooleanField(default=False)  # Mini kitchen
    heating = models.BooleanField(default=False)

    #Campfire
    campfire_access = models.BooleanField(
        default=False,
        help_text="Is there access to a campfire pit?"
    )
    outdoor_shower = models.BooleanField(
        default=False,
        help_text="Is there an outdoor shower available?"
    )
    portable_restroom = models.BooleanField(
        default=False,
        help_text="Is there access to a portable restroom?"
    )
    rv_hookup = models.BooleanField(
        default=False,
        help_text="Is an RV electrical hookup available?"
    )
    eco_friendly_facilities = models.BooleanField(
        default=False,
        help_text="Are eco-friendly facilities available?"
    )
    barbecue_grill = models.BooleanField(
        default=False,
        help_text="Is a barbecue grill provided?"
    )
    picnic_area = models.BooleanField(
        default=False,
        help_text="Is there a designated picnic area?"
    )
    hammock = models.BooleanField(
        default=False,
        help_text="Is a hammock available?"
    )
    outdoor_seating = models.BooleanField(
        default=False,
        help_text="Is there outdoor seating (e.g., benches, chairs)?"
    )
    nature_trail_access = models.BooleanField(
        default=False,
        help_text="Does the site have direct access to nature or hiking trails?"
    )

    def __str__(self):
        return f"Room Amenities (Wi-Fi: {self.free_wifi}, TV: {self.television})"


class RoomType(models.Model):
    """
    Model to define room types and their properties.
    """
    ROOM_TYPE_CHOICES = [
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('twin', 'Twin Room'),
        ('suite', 'Suite'),
        ('studio', 'Studio'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('cottage', 'Cottage'),
        ('bungalow', 'Bungalow'),
        ('family', 'Family Room'),
        ('deluxe', 'Deluxe Room'),
        ('penthouse', 'Penthouse'),
        ('dormitory', 'Dormitory'),
        ('camping_site', 'Camping Site'),
        ('glamping_tent', 'Glamping Tent'),
        ('rv_spot', 'RV Spot'),
    ]
    ROOM_NAME_CHOICES = [
    # Basic Rooms
    ('single_room', 'Single Room'),
    ('double_room', 'Double Room'),
    ('twin_room', 'Twin Room'),
    ('family_room', 'Family Room'),
    ('deluxe_room', 'Deluxe Room'),
    ('suite', 'Suite'),
    ('studio', 'Studio'),
    ('apartment', 'Apartment'),
    ('villa', 'Villa'),
    ('cottage', 'Cottage'),
    ('bungalow', 'Bungalow'),
    ('dormitory', 'Dormitory'),
    ('penthouse', 'Penthouse'),

    # Rooms with Views
    ('single_room_with_garden_view', 'Single Room with Garden View'),
    ('double_room_with_sea_view', 'Double Room with Sea View'),
    ('suite_with_mountain_view', 'Suite with Mountain View'),
    ('family_room_with_city_view', 'Family Room with City View'),
    ('deluxe_room_with_landmark_view', 'Deluxe Room with Landmark View'),
    ('penthouse_with_panorama_view', 'Penthouse with Panorama View'),

    # Rooms with Balconies
    ('single_room_with_balcony', 'Single Room with Balcony'),
    ('double_room_with_balcony', 'Double Room with Balcony'),
    ('suite_with_balcony', 'Suite with Balcony'),
    ('family_room_with_balcony', 'Family Room with Balcony'),
    ('deluxe_room_with_balcony', 'Deluxe Room with Balcony'),
    ('king_room_with_balcony', 'King Room with Balcony'),

    #deluxe_rooms
    ('deluxe_room_with_garden_view', 'Deluxe Room with Garden View'),
    ('deluxe_king_room', 'Deluxe King Room'),
    ('deluxe_family_room', 'Deluxe Family Room'),
    ('super_deluxe_room_with_lake_view', 'Super Deluxe Room with Lake View'),
    ('super_deluxe_room_with_city_view', 'Super Deluxe Room with City View'),
    ('deluxe_room_with_view_room', 'Deluxe Room with View Room'),
    ('deluxe_room_with_city_view', 'Deluxe Room with City View'),
    ('simple Deluxe Room', 'Simple Deluxe Room'),
   

    # Rooms with Special Features
    ('single_room_with_balcony', 'Single Room with Balcony'),
    ('double_room_with_terrace', 'Double Room with Terrace'),
    ('suite_with_private_pool', 'Suite with Private Pool'),
    ('family_room_with_kitchenette', 'Family Room with Kitchenette'),
    ('deluxe_room_with_hot_tub', 'Deluxe Room with Hot Tub'),
    ('apartment_with_two_bedrooms', 'Apartment with Two Bedrooms'),
    ('villa_with_private_beach', 'Villa with Private Beach'),
    ('bungalow_with_hammock', 'Bungalow with Hammock'),
    ('studio_with_rooftop_access', 'Studio with Rooftop Access'),

    # Accessible Rooms
    ('accessible_single_room', 'Accessible Single Room'),
    ('accessible_double_room', 'Accessible Double Room'),
    ('accessible_suite', 'Accessible Suite'),

    # Economy Rooms
    ('budget_single_room', 'Budget Single Room'),
    ('budget_double_room', 'Budget Double Room'),
    ('economy_family_room', 'Economy Family Room'),
    ('basic_dormitory_bed', 'Basic Dormitory Bed'),

    # Luxury Rooms
    ('luxury_penthouse_with_pool', 'Luxury Penthouse with Pool'),
    ('royal_suite_with_terrace', 'Royal Suite with Terrace'),
    ('executive_suite_with_office', 'Executive Suite with Office'),

    # Thematic Rooms
    ('jungle_theme_room', 'Jungle Theme Room'),
    ('ocean_theme_room', 'Ocean Theme Room'),
    ('romantic_suite', 'Romantic Suite'),
    ('adventure_room', 'Adventure Room'),

    # Special Configurations
    ('triple_room', 'Triple Room'),
    ('quad_room', 'Quad Room'),
    ('interconnected_room', 'Interconnected Room'),
    ('loft_room', 'Loft Room'),
    ('mezzanine_room', 'Mezzanine Room'),

    # Other Options
    ('standard_room', 'Standard Room'),
    ('superior_room', 'Superior Room'),
    ('premium_room', 'Premium Room'),
    ('presidential_suite', 'Presidential Suite'),

    # Custom Room Names
    ('camping_site', 'Camping Site'),
    ('glamping_tent', 'Glamping Tent'),
    ('rv_spot', 'RV Spot'),
    ('camping_cabin', 'Camping Cabin'),
    ('treehouse', 'Treehouse'),
    ('eco_hut', 'Eco Hut'),
    ('yurt', 'Yurt'),
    ('tipi', 'Tipi'),
    ('safari_tent', 'Safari Tent'),
    ('overland_vehicle_site', 'Overland Vehicle Site'),
    ('tent_with_campfire', 'Tent with Campfire Access'),
    ('luxury_glamping_tent', 'Luxury Glamping Tent'),
    ('camping_site_with_amenities', 'Camping Site with Amenities'),
]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    property=models.ForeignKey('property.Property',on_delete=models.CASCADE, 
        related_name="room_type")
    room_type = models.CharField(
        max_length=50, 
        choices=ROOM_TYPE_CHOICES, 
        help_text="Type of room (e.g., Single Room, Suite)"
    )
    room_name = models.CharField(
        max_length=255,
        choices=ROOM_NAME_CHOICES,
        help_text="Descriptive name for the room visible to guests"
    )
    # no_of_available_rooms = models.PositiveIntegerField(
    #     default=1, 
    #     help_text="Number of rooms available of this type"
    # )
    max_no_of_guests = models.PositiveIntegerField(
        help_text="Maximum number of guests allowed in this room"
    )
    room_size = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="Room size in square meters"
    )
    smoking_allowed = models.BooleanField(
        default=False, 
        help_text="Indicates if smoking is allowed in this room"
    )
    room_amenities = models.OneToOneField(
        RoomAmenities, 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="single_room_amenities"
    )


    def __str__(self):
        return f"{self.property.property_name} - {self.get_room_type_display()} - {self.room_name}"


class RoomBed(models.Model):
    """
    Model to associate bed types with their quantities to a specific room type.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="room_beds")
    bed_type = models.ForeignKey(BedType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(help_text="Number of beds of this type in the room")

    class Meta:
        unique_together = ('room_type', 'bed_type')

    def __str__(self):
        return f"{self.quantity} x {self.bed_type} in {self.room_type}for {self.room_type.property.property_name}"


class Price(models.Model):
    """
    Model to handle pricing for properties or rooms.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Link to RoomType or Property
    room_type = models.ForeignKey(
        'RoomType',
        on_delete=models.CASCADE,
        related_name='prices',
        null=True,
        blank=True,
        help_text="Room type this price is associated with (optional)."
    )
    property = models.ForeignKey(
        'property.Property',
        on_delete=models.CASCADE,
        related_name='prices',
        null=True,
        blank=True,
        help_text="Property this price is associated with (optional)."
    )
    
    # Price Fields
    base_price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Base price per night in the default currency."
    )
    extra_guest_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Price for additional guests beyond the max capacity (per guest, per night)."
    )
    breakfast_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Extra cost for breakfast, if not included."
    )
    parking_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Cost for parking, if applicable."
    )

    # Seasonal and Promotional Pricing
    is_seasonal = models.BooleanField(
        default=False,
        help_text="Indicates if this pricing is seasonal."
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        help_text="Start date for seasonal pricing."
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="End date for seasonal pricing."
    )
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        blank=True,
        help_text="Discount percentage applied to the base price."
    )

    # Currency
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        help_text="Currency associated with this price.",
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__lte=models.F('end_date')),
                name="valid_seasonal_date_range"
            )
        ]

    def calculate_final_price(self, num_guests=1, include_breakfast=False, include_parking=False):
        price = self.base_price_per_night
        if num_guests > 1:
            price += self.extra_guest_price * (num_guests - 1)
        
        # Add optional breakfast cost
        if include_breakfast:
            price += self.breakfast_price
        
        # Add parking cost
        if include_parking:
            price += self.parking_price
        
        # Apply discount
        if self.discount_percentage > 0:
            discount = price * (self.discount_percentage / 100)
            price -= discount
        
        return round(price, 2)

    def is_active(self):
        today = date.today()
        if self.is_seasonal:
            return self.start_date <= today <= self.end_date
        return True

    def __str__(self):
        if self.room_type:
            return f"Price for {self.room_type} - {self.base_price_per_night} {self.currency}"
        elif self.property:
            return f"Price for {self.property} - {self.base_price_per_night} {self.currency}"
        return f"General Price - {self.base_price_per_night} {self.currency}"
    
class RoomImages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_type=models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="images")
    image=models.ImageField(upload_to='rooms/',null=True,blank=True)

############Roomavailability##################

class RoomAvailability(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="availabilities", help_text="Room type for this availability")
    date = models.DateField(help_text="Date for room availability",null=True,blank=True)
    available_rooms = models.PositiveIntegerField(default=0, help_text="Number of available rooms for this date",null=True,blank=True)

    class Meta:
        unique_together = ('room_type', 'date') 
        ordering = ['date']

    def __str__(self):
        return f"{self.room_type.room_name} - {self.date}: {self.available_rooms} available"