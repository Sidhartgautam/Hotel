# Generated by Django 5.0.7 on 2025-03-03 09:43

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyReview',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('rating', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GuestReview',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('staff', models.FloatField()),
                ('facilities', models.FloatField()),
                ('cleanliness', models.FloatField()),
                ('comfort', models.FloatField()),
                ('value_for_money', models.FloatField()),
                ('location', models.FloatField()),
                ('free_wifi', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_reviews', to='property.property')),
            ],
        ),
    ]
