import csv
import json
import uuid
from decimal import Decimal
from django.core.management.base import BaseCommand
from country.models import Country, City
from currency.models import Currency
from users.models import User
from property.models import Property
from rooms.models import (
    RoomType, RoomAmenities, RoomBed, BedType, Price, RoomImages
)


class Command(BaseCommand):
    help = "Bulk import room details for hotels from CSV"

    def handle(self, *args, **kwargs):
        file_path = "pokhara_hotel_rooms.csv"  # Ensure this file is in your Django root directory

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                rooms_to_create = []
                room_amenities_to_create = []
                room_beds_to_create = []
                room_prices_to_create = []
                room_images_to_create = []

                for row in reader:
                    try:
                        # Get the Property (Hotel)
                        property_obj = Property.objects.filter(property_name=row["property_name"]).first()
                        if not property_obj:
                            self.stdout.write(self.style.WARNING(f"Skipping room entry. Property not found: {row['property_name']}"))
                            continue

                        # Create RoomType
                        room_type_obj = RoomType(
                            id=uuid.uuid4(),
                            property=property_obj,
                            room_type=row["room_type"],
                            room_name=row["room_name"],
                            no_of_available_rooms=int(row["no_of_available_rooms"]),
                            max_no_of_guests=int(row["max_no_of_guests"]),
                            room_size=Decimal(row["room_size"]),
                            smoking_allowed=row["smoking_allowed"] == "True",
                        )
                        rooms_to_create.append(room_type_obj)

                        # Create RoomAmenities
                        room_amenities_obj = RoomAmenities(
                            id=uuid.uuid4(),
                            room_type=room_type_obj,
                            air_conditioning=row["air_conditioning"] == "True",
                            free_wifi=row["free_wifi"] == "True",
                            television=row["television"] == "True",
                            minibar=row["minibar"] == "True",
                            wardrobe=row["wardrobe"] == "True",
                            desk=row["desk"] == "True",
                            telephone=row["telephone"] == "True",
                            safe=row["safe"] == "True",
                            soundproofing=row["soundproofing"] == "True",
                            ironing_facilities=row["ironing_facilities"] == "True",
                            extra_long_beds=row["extra_long_beds"] == "True",
                            electric_blankets=row["electric_blankets"] == "True",
                            garden_view=row["garden_view"] == "True",
                            city_view=row["city_view"] == "True",
                            mountain_view=row["mountain_view"] == "True",
                            landmark_view=row["landmark_view"] == "True",
                            pool_view=row["pool_view"] == "True",
                            attached_bathroom=row["attached_bathroom"] == "True",
                            free_toiletries=row["free_toiletries"] == "True",
                            shower=row["shower"] == "True",
                            bathtub=row["bathtub"] == "True",
                            balcony=row["balcony"] == "True",
                            patio=row["patio"] == "True",
                            terrace=row["terrace"] == "True",
                            private_entrance=row["private_entrance"] == "True",
                            kitchenette=row["kitchenette"] == "True",
                            heating=row["heating"] == "True",
                        )
                        room_amenities_to_create.append(room_amenities_obj)

                        # Create RoomBeds
                        bed_data = json.loads(row["beds"].replace("'", '"')) if row["beds"].strip() else []
                        for bed in bed_data:
                            bed_type_obj, _ = BedType.objects.get_or_create(bed_type=bed["bed_type"])
                            room_beds_to_create.append(RoomBed(
                                room_type=room_type_obj,
                                bed_type=bed_type_obj,
                                quantity=int(bed["quantity"])
                            ))

                        # Create Room Price
                        room_prices_to_create.append(Price(
                            room_type=room_type_obj,
                            property=property_obj,
                            base_price_per_night=Decimal(row["base_price_per_night"]),
                            extra_guest_price=Decimal(row["extra_guest_price"]),
                            breakfast_price=Decimal(row["breakfast_price"]),
                            parking_price=Decimal(row["parking_price"]),
                            is_seasonal=row["is_seasonal"] == "True",
                            start_date=row["start_date"] if row["start_date"] else None,
                            end_date=row["end_date"] if row["end_date"] else None,
                            discount_percentage=Decimal(row["discount_percentage"]),
                            currency=Currency.objects.filter(currency_code=row["currency"]).first(),
                        ))

                        # Room Images
                        image_list = json.loads(row["images"].replace("'", '"')) if row["images"].strip() else []
                        for img_url in image_list:
                            room_images_to_create.append(RoomImages(
                                room_type=room_type_obj,
                                image=img_url
                            ))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Skipping room entry due to error: {e}"))

                # Bulk insert for efficiency
                RoomType.objects.bulk_create(rooms_to_create)
                RoomAmenities.objects.bulk_create(room_amenities_to_create)
                RoomBed.objects.bulk_create(room_beds_to_create)
                Price.objects.bulk_create(room_prices_to_create)
                RoomImages.objects.bulk_create(room_images_to_create)

                self.stdout.write(self.style.SUCCESS("Successfully imported room details for hotels"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("CSV file not found. Ensure 'pokhara_hotel_rooms.csv' exists in the project root."))
