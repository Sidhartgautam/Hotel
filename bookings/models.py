from django.db import models
from datetime import date
import uuid
from rooms.models import RoomType  # Adjust the import based on your app structure
from property.models import Property  # Adjust this import as needed

class Booking(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Arrival'),
        ('stripe', 'Stripe'),
        ('moredeals', 'MoreDeals'),
    ]
    CANCELLATION_STATUS_CHOICES = [
        ('not_canceled', 'Not Canceled'),
        ('canceled', 'Canceled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('pending', 'Pending'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey('users.User',on_delete=models.CASCADE,related_name="bookings",help_text="The user who made the booking.",null=True,blank=True)
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="bookings",
        help_text="The property this booking belongs to.",
    )
    room = models.ForeignKey(
        RoomType,
        on_delete=models.CASCADE,
        related_name="bookings",
        help_text="The room type this booking is for.",
    )
    check_in = models.DateField(help_text="Check-in date for the booking.")
    check_out = models.DateField(help_text="Check-out date for the booking.")
    num_guests = models.PositiveIntegerField(help_text="Number of guests for the booking.")
    customer_name = models.CharField(max_length=255, help_text="Name of the customer.")
    customer_email = models.EmailField(help_text="Email of the customer.")
    guest_status = models.CharField(max_length=20, choices=[('checked_in', 'Checked In'), ('checked_out', 'Checked Out')],null=True,blank=True)
    booking_date = models.DateField(auto_now_add=True, help_text="Date when the booking was made.")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES,null=True,blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending',null=True,blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    cancellation_status = models.CharField(
        max_length=20,
        choices=CANCELLATION_STATUS_CHOICES,
        default='not_canceled',
        help_text="Indicates if the booking has been canceled.",
        null=True,
        blank=True
    )
    cancellation_date = models.DateField(null=True, blank=True, help_text="Date when the booking was canceled.")

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(check_in__lt=models.F("check_out")),
                name="valid_check_in_out_dates",
            )
        ]

    def __str__(self):
        return f"Booking for {self.room.room_name} ({self.check_in} to {self.check_out})"
