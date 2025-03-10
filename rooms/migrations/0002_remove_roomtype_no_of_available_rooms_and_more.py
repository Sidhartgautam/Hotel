# Generated by Django 5.0.7 on 2025-03-05 13:46

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomtype',
            name='no_of_available_rooms',
        ),
        migrations.CreateModel(
            name='RoomAvailability',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True, help_text='Date for room availability', null=True)),
                ('available_rooms', models.PositiveIntegerField(blank=True, default=0, help_text='Number of available rooms for this date', null=True)),
                ('room_type', models.ForeignKey(help_text='Room type for this availability', on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to='rooms.roomtype')),
            ],
            options={
                'ordering': ['date'],
                'unique_together': {('room_type', 'date')},
            },
        ),
    ]
