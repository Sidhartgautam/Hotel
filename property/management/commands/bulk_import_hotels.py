import csv
import json
import uuid
from decimal import Decimal
from django.core.management.base import BaseCommand
from country.models import Country, City
from currency.models import Currency
from users.models import User
from property.models import (
    Property, PropertyCategory, PropertyImage, Amenity, PropertyAmenities,
    Policy, CancellationPolicy, SingleUnitPrice
)
from core.utils.slugify import unique_slug_generator

class Command(BaseCommand):
    help = "Bulk import Pokhara hotel data from CSV"

    def handle(self, *args, **kwargs):
        file_path = "pokhara_hotels.csv"  # Ensure this file is in your Django root directory

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                properties_to_create = []
                images_to_create = []
                amenities_to_create = []
                policies_to_create = []
                cancellation_policies_to_create = []
                single_unit_prices_to_create = []

                for row in reader:
                    try:
                        # Get or create Country using correct field
                        country, _ = Country.objects.get_or_create(country_name=row["country"])

                        # Get or create City using correct field
                        city, _ = City.objects.get_or_create(city_name=row["city"], country=country)

                        # Get or create Currency using correct field
                        currency, _ = Currency.objects.get_or_create(currency_code=row["currency"])

                        # Get or create User
                        user, _ = User.objects.get_or_create(email=row["user_email"], defaults={"username": row["user_email"].split('@')[0]})

                        # Get or create Property Category
                        category, _ = PropertyCategory.objects.get_or_create(category_name=row["category"])

                        # Create Property without slug first
                        property_obj = Property(
                            id=uuid.uuid4(),
                            property_name=row["property_name"],
                            is_single_unit=row["is_single_unit"] == "True",
                            address=row["address"],
                            description=row["description"],
                            star_rating_property=int(row["star_rating"]),
                            country=country,
                            city=city,
                            currency=currency,
                            state=row["state"],
                            lng=Decimal(row["lng"]) if row["lng"] else None,
                            lat=Decimal(row["lat"]) if row["lat"] else None,
                            user=user,
                            category=category,
                            language=row["language"],
                        )

                        # Now generate the slug after creating the instance
                        property_obj.slug = unique_slug_generator(property_obj)

                        properties_to_create.append(property_obj)

                        # Property Images
                        try:
                            image_list = json.loads(row["images"].replace("'", '"')) if row["images"].strip() else []
                        except json.JSONDecodeError:
                            image_list = []
                            self.stdout.write(self.style.WARNING(f"Invalid JSON in images for {row['property_name']}"))

                        for img_url in image_list:
                            images_to_create.append(PropertyImage(property=property_obj, image=img_url))

                        # Handle amenities safely
                        amenities_data = row["amenities"].strip()  # Remove extra spaces
                        if not amenities_data or amenities_data == "null":
                            amenities_list = []  # Set to empty list if missing
                        else:
                            try:
                                amenities_list = json.loads(amenities_data.replace("'", '"'))  # Replace single quotes with double quotes
                            except json.JSONDecodeError:
                                self.stdout.write(self.style.ERROR(f"Skipping row due to invalid JSON in amenities: {amenities_data}"))
                                continue  # Skip this row and move to the next

                        # Process each amenity
                        for amenity_name in amenities_list:
                            amenity, _ = Amenity.objects.get_or_create(name=amenity_name)
                            amenities_to_create.append(PropertyAmenities(property=property_obj, amenity=amenity))

                        # Policy
                        policies_to_create.append(
                            Policy(
                                property=property_obj,
                                checkin_time_from=row["checkin_time_from"],
                                checkin_time_to=row["checkin_time_to"],
                                checkout_time_from=row["checkout_time_from"],
                                checkout_time_to=row["checkout_time_to"],
                                children_allowed=row["children_allowed"] == "True",
                                extra_beds_available=row["extra_beds_available"] == "True",
                                extra_bed_cost=Decimal(row["extra_bed_cost"]) if row["extra_bed_cost"] else None,
                                pets_allowed=row["pets_allowed"] == "True",
                                pet_fee=Decimal(row["pet_fee"]) if row["pet_fee"] else None,
                                pet_details=row["pet_details"] if row["pet_details"] else None,
                            )
                        )

                        # Cancellation Policy
                        cancellation_policies_to_create.append(
                            CancellationPolicy(
                                property=property_obj,
                                cancellations_allowed=row["cancellations_allowed"] == "True",
                                cancellation_deadline_days=int(row["cancellation_deadline_days"]),
                                cancellation_fee_type=row["cancellation_fee_type"],
                                cancellation_fee_amount=Decimal(row["cancellation_fee_amount"]) if row["cancellation_fee_amount"] else None,
                                refundable=row["refundable"] == "True",
                                additional_notes=row["additional_notes"],
                            )
                        )

                        # Single Unit Price
                        single_unit_prices_to_create.append(
                            SingleUnitPrice(
                                property=property_obj,
                                base_price_per_night=Decimal(row["base_price_per_night"]),
                                seasonal_price=Decimal(row["seasonal_price"]) if row["seasonal_price"] else None,
                                discount_percentage=float(row["discount_percentage"]),
                                currency=currency,
                            )
                        )

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Skipping row due to error: {e}"))

                # Bulk insert for efficiency
                Property.objects.bulk_create(properties_to_create)
                PropertyImage.objects.bulk_create(images_to_create)
                PropertyAmenities.objects.bulk_create(amenities_to_create)
                Policy.objects.bulk_create(policies_to_create)
                CancellationPolicy.objects.bulk_create(cancellation_policies_to_create)
                SingleUnitPrice.objects.bulk_create(single_unit_prices_to_create)

                self.stdout.write(self.style.SUCCESS("Successfully imported Pokhara hotels data"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("CSV file not found. Ensure 'pokhara_hotels.csv' exists in the project root."))
