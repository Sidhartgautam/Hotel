from property.models import Amenity

# List of all possible amenities
bulk_amenities = [
    # General Amenities
    "Free Wi-Fi", "24/7 Security", "Parking", "Air Conditioning", "Heating", 
    "Room Service", "Mini Bar", "Flat-screen TV", "Balcony/Terrace", "Elevator", 
    "Smoking Area", "Pet Friendly", "Laundry Service", "Daily Housekeeping", 
    "Concierge Service", "Luggage Storage", "In-room Safe", "Coffee/Tea Maker", 
    "Hair Dryer", "Iron/Ironing Board",

    # Leisure & Recreation Amenities
    "Swimming Pool", "Gym/Fitness Center", "Spa Services", "Sauna", "Hot Tub/Jacuzzi", 
    "Game Room", "Tennis Court", "Golf Course", "Yoga/Meditation Area", 
    "Private Beach Access", "Garden/Lawn", "Barbecue Facilities", "Cinema Room", "Library",

    # Business & Meeting Facilities
    "Conference Room", "Business Center", "Meeting Rooms", "Printing/Copy Services", 
    "High-Speed Internet", "Event Space",

    # Food & Beverage Amenities
    "On-site Restaurant", "Bar/Lounge", "Breakfast Included", "Room Service", 
    "Vending Machines", "Coffee Shop", "Poolside Bar", "Snack Bar",

    # Transportation & Accessibility
    "Airport Shuttle", "Free Parking", "Valet Parking", "Onsite Parking", 
    "Wheelchair Accessible", "Car Rental Services", "Bicycle Rental",

    # Family & Child-Friendly Amenities
    "Children’s Play Area", "Kids Club", "Babysitting Services", "Family Rooms", 
    "Child Safety Gates", "Children's Pool",

    # Health & Wellness
    "Massage Services", "Wellness Center", "Personal Trainer", "Steam Room", 
    "Meditation Room", "Detox Programs",

    # Sustainability & Eco-Friendly Amenities
    "Solar Power", "Energy-efficient Appliances", "Rainwater Harvesting", 
    "Recycling Bins", "Electric Vehicle Charging Stations", "Organic Toiletries",

    # Technology & Entertainment
    "Smart TV with Streaming Services", "Surround Sound System", 
    "High-Speed Internet (Fiber)", "Virtual Reality Room", "Interactive Games", 
    "Smart Room Controls (Lights, Curtains, AC)",

    # Property-Specific Amenities (Luxury & Unique Features)
    "Private Pool", "Rooftop Deck", "Helipad", "Wine Cellar", "Fireplace", 
    "Butler Service", "Private Chef", "Infinity Pool", "Observatory (Telescope)",

    # Utility & Safety Amenities
    "Backup Generator", "Fire Extinguishers", "First Aid Kit", "Smoke Alarms", 
    "Carbon Monoxide Detectors", "24-hour Emergency Services"
]

# Add amenities to the database
for amenity_name in bulk_amenities:
    amenity, created = Amenity.objects.get_or_create(name=amenity_name)
    if created:
        print(f"Added: {amenity_name}")
    else:
        print(f"Already exists: {amenity_name}")
