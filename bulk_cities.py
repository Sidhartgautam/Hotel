import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")  # Update with your project name
django.setup()

from property.models import City, Country
import uuid

# Define the list of cities in Sweden
sweden_cities_data = [
    {"city_name": "Stockholm", "country_code": "SE"},
    {"city_name": "Gothenburg", "country_code": "SE"},
    {"city_name": "Malmö", "country_code": "SE"},
    {"city_name": "Uppsala", "country_code": "SE"},
    {"city_name": "Västerås", "country_code": "SE"},
    {"city_name": "Örebro", "country_code": "SE"},
]

# Get the Sweden country instance (Ensure Sweden exists in DB)
for city_data in sweden_cities_data:
    try:
        country = Country.objects.get(country_code=city_data["country_code"])
        # Check if the city already exists to avoid duplicates
        city, created = City.objects.get_or_create(
            city_name=city_data["city_name"],
            country=country,
            defaults={"id": uuid.uuid4()}  # Assign unique UUID if new
        )
        if created:
            print(f"✅ Added city: {city.city_name} in {country.country_name}")
        else:
            print(f"⚠️ City already exists: {city.city_name}")

    except Country.DoesNotExist:
        print(f"❌ Error: Country with code {city_data['country_code']} not found!")

print("✅ Bulk insert process for Sweden completed.")
