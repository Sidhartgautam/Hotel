# Generated by Django 5.0.7 on 2025-03-03 09:43

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('currency', '0001_initial'),
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BedType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bed_type', models.CharField(choices=[('single_bed', 'Single Bed'), ('double_bed', 'Double Bed'), ('queen_bed', 'Queen Bed'), ('king_bed', 'King Bed'), ('sofa_bed', 'Sofa Bed'), ('bunk_bed', 'Bunk Bed'), ('futon', 'Futon'), ('crib', 'Crib'), ('twin_beds', 'Twin Beds'), ('triple_beds', 'Triple Beds'), ('quad_beds', 'Quad Beds'), ('octuple_beds', 'Octuple Beds'), ('full_beds', 'Full Beds')], max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomAmenities',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('air_conditioning', models.BooleanField(default=False)),
                ('free_wifi', models.BooleanField(default=False)),
                ('television', models.BooleanField(default=False)),
                ('minibar', models.BooleanField(default=False)),
                ('wardrobe', models.BooleanField(default=False)),
                ('desk', models.BooleanField(default=False)),
                ('telephone', models.BooleanField(default=False)),
                ('safe', models.BooleanField(default=False)),
                ('soundproofing', models.BooleanField(default=False)),
                ('ironing_facilities', models.BooleanField(default=False)),
                ('extra_long_beds', models.BooleanField(default=False)),
                ('electric_blankets', models.BooleanField(default=False)),
                ('garden_view', models.BooleanField(default=False)),
                ('city_view', models.BooleanField(default=False)),
                ('mountain_view', models.BooleanField(default=False)),
                ('landmark_view', models.BooleanField(default=False)),
                ('pool_view', models.BooleanField(default=False)),
                ('attached_bathroom', models.BooleanField(default=False)),
                ('free_toiletries', models.BooleanField(default=False)),
                ('shower', models.BooleanField(default=False)),
                ('bathtub', models.BooleanField(default=False)),
                ('bidet', models.BooleanField(default=False)),
                ('hairdryer', models.BooleanField(default=False)),
                ('slippers', models.BooleanField(default=False)),
                ('towels', models.BooleanField(default=False)),
                ('toilet', models.BooleanField(default=False)),
                ('balcony', models.BooleanField(default=False)),
                ('patio', models.BooleanField(default=False)),
                ('terrace', models.BooleanField(default=False)),
                ('private_entrance', models.BooleanField(default=False)),
                ('kitchenette', models.BooleanField(default=False)),
                ('heating', models.BooleanField(default=False)),
                ('campfire_access', models.BooleanField(default=False, help_text='Is there access to a campfire pit?')),
                ('outdoor_shower', models.BooleanField(default=False, help_text='Is there an outdoor shower available?')),
                ('portable_restroom', models.BooleanField(default=False, help_text='Is there access to a portable restroom?')),
                ('rv_hookup', models.BooleanField(default=False, help_text='Is an RV electrical hookup available?')),
                ('eco_friendly_facilities', models.BooleanField(default=False, help_text='Are eco-friendly facilities available?')),
                ('barbecue_grill', models.BooleanField(default=False, help_text='Is a barbecue grill provided?')),
                ('picnic_area', models.BooleanField(default=False, help_text='Is there a designated picnic area?')),
                ('hammock', models.BooleanField(default=False, help_text='Is a hammock available?')),
                ('outdoor_seating', models.BooleanField(default=False, help_text='Is there outdoor seating (e.g., benches, chairs)?')),
                ('nature_trail_access', models.BooleanField(default=False, help_text='Does the site have direct access to nature or hiking trails?')),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('room_type', models.CharField(choices=[('single', 'Single Room'), ('double', 'Double Room'), ('twin', 'Twin Room'), ('suite', 'Suite'), ('studio', 'Studio'), ('apartment', 'Apartment'), ('villa', 'Villa'), ('cottage', 'Cottage'), ('bungalow', 'Bungalow'), ('family', 'Family Room'), ('deluxe', 'Deluxe Room'), ('penthouse', 'Penthouse'), ('dormitory', 'Dormitory'), ('camping_site', 'Camping Site'), ('glamping_tent', 'Glamping Tent'), ('rv_spot', 'RV Spot')], help_text='Type of room (e.g., Single Room, Suite)', max_length=50)),
                ('room_name', models.CharField(choices=[('single_room', 'Single Room'), ('double_room', 'Double Room'), ('twin_room', 'Twin Room'), ('family_room', 'Family Room'), ('deluxe_room', 'Deluxe Room'), ('suite', 'Suite'), ('studio', 'Studio'), ('apartment', 'Apartment'), ('villa', 'Villa'), ('cottage', 'Cottage'), ('bungalow', 'Bungalow'), ('dormitory', 'Dormitory'), ('penthouse', 'Penthouse'), ('single_room_with_garden_view', 'Single Room with Garden View'), ('double_room_with_sea_view', 'Double Room with Sea View'), ('suite_with_mountain_view', 'Suite with Mountain View'), ('family_room_with_city_view', 'Family Room with City View'), ('deluxe_room_with_landmark_view', 'Deluxe Room with Landmark View'), ('penthouse_with_panorama_view', 'Penthouse with Panorama View'), ('deluxe_room_with_garden_view', 'Deluxe Room with Garden View'), ('super_deluxe_room_with_lake_view', 'Super Deluxe Room with Lake View'), ('super_deluxe_room_with_city_view', 'Super Deluxe Room with City View'), ('deluxe_room_with_view_room', 'Deluxe Room with View Room'), ('deluxe_room_with_city_view', 'Deluxe Room with City View'), ('simple Deluxe Room', 'Simple Deluxe Room'), ('single_room_with_balcony', 'Single Room with Balcony'), ('double_room_with_terrace', 'Double Room with Terrace'), ('suite_with_private_pool', 'Suite with Private Pool'), ('family_room_with_kitchenette', 'Family Room with Kitchenette'), ('deluxe_room_with_hot_tub', 'Deluxe Room with Hot Tub'), ('apartment_with_two_bedrooms', 'Apartment with Two Bedrooms'), ('villa_with_private_beach', 'Villa with Private Beach'), ('bungalow_with_hammock', 'Bungalow with Hammock'), ('studio_with_rooftop_access', 'Studio with Rooftop Access'), ('accessible_single_room', 'Accessible Single Room'), ('accessible_double_room', 'Accessible Double Room'), ('accessible_suite', 'Accessible Suite'), ('budget_single_room', 'Budget Single Room'), ('budget_double_room', 'Budget Double Room'), ('economy_family_room', 'Economy Family Room'), ('basic_dormitory_bed', 'Basic Dormitory Bed'), ('luxury_penthouse_with_pool', 'Luxury Penthouse with Pool'), ('royal_suite_with_terrace', 'Royal Suite with Terrace'), ('executive_suite_with_office', 'Executive Suite with Office'), ('jungle_theme_room', 'Jungle Theme Room'), ('ocean_theme_room', 'Ocean Theme Room'), ('romantic_suite', 'Romantic Suite'), ('adventure_room', 'Adventure Room'), ('triple_room', 'Triple Room'), ('quad_room', 'Quad Room'), ('interconnected_room', 'Interconnected Room'), ('loft_room', 'Loft Room'), ('mezzanine_room', 'Mezzanine Room'), ('standard_room', 'Standard Room'), ('superior_room', 'Superior Room'), ('premium_room', 'Premium Room'), ('presidential_suite', 'Presidential Suite'), ('camping_site', 'Camping Site'), ('glamping_tent', 'Glamping Tent'), ('rv_spot', 'RV Spot'), ('camping_cabin', 'Camping Cabin'), ('treehouse', 'Treehouse'), ('eco_hut', 'Eco Hut'), ('yurt', 'Yurt'), ('tipi', 'Tipi'), ('safari_tent', 'Safari Tent'), ('overland_vehicle_site', 'Overland Vehicle Site'), ('tent_with_campfire', 'Tent with Campfire Access'), ('luxury_glamping_tent', 'Luxury Glamping Tent'), ('camping_site_with_amenities', 'Camping Site with Amenities')], help_text='Descriptive name for the room visible to guests', max_length=255)),
                ('no_of_available_rooms', models.PositiveIntegerField(default=1, help_text='Number of rooms available of this type')),
                ('max_no_of_guests', models.PositiveIntegerField(help_text='Maximum number of guests allowed in this room')),
                ('room_size', models.DecimalField(decimal_places=2, help_text='Room size in square meters', max_digits=5)),
                ('smoking_allowed', models.BooleanField(default=False, help_text='Indicates if smoking is allowed in this room')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_type', to='property.property')),
                ('room_amenities', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='single_room_amenities', to='rooms.roomamenities')),
            ],
        ),
        migrations.CreateModel(
            name='RoomImages',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='rooms/')),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='rooms.roomtype')),
            ],
        ),
        migrations.AddField(
            model_name='roomamenities',
            name='room_type',
            field=models.ForeignKey(blank=True, help_text='Room type that these amenities belong to', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='all_room_amenities', to='rooms.roomtype'),
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('base_price_per_night', models.DecimalField(decimal_places=2, help_text='Base price per night in the default currency.', max_digits=10)),
                ('extra_guest_price', models.DecimalField(decimal_places=2, default=0.0, help_text='Price for additional guests beyond the max capacity (per guest, per night).', max_digits=10)),
                ('breakfast_price', models.DecimalField(decimal_places=2, default=0.0, help_text='Extra cost for breakfast, if not included.', max_digits=10)),
                ('parking_price', models.DecimalField(decimal_places=2, default=0.0, help_text='Cost for parking, if applicable.', max_digits=10)),
                ('is_seasonal', models.BooleanField(default=False, help_text='Indicates if this pricing is seasonal.')),
                ('start_date', models.DateField(blank=True, help_text='Start date for seasonal pricing.', null=True)),
                ('end_date', models.DateField(blank=True, help_text='End date for seasonal pricing.', null=True)),
                ('discount_percentage', models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='Discount percentage applied to the base price.', max_digits=5)),
                ('currency', models.ForeignKey(blank=True, help_text='Currency associated with this price.', null=True, on_delete=django.db.models.deletion.CASCADE, to='currency.currency')),
                ('property', models.ForeignKey(blank=True, help_text='Property this price is associated with (optional).', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='property.property')),
                ('room_type', models.ForeignKey(blank=True, help_text='Room type this price is associated with (optional).', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='rooms.roomtype')),
            ],
        ),
        migrations.CreateModel(
            name='RoomBed',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(help_text='Number of beds of this type in the room')),
                ('bed_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.bedtype')),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_beds', to='rooms.roomtype')),
            ],
            options={
                'unique_together': {('room_type', 'bed_type')},
            },
        ),
        migrations.AddConstraint(
            model_name='price',
            constraint=models.CheckConstraint(check=models.Q(('start_date__lte', models.F('end_date'))), name='valid_seasonal_date_range'),
        ),
    ]
