from rest_framework import serializers
from property.models import Property 
from django.db.models import Avg,F
from django.db import models
from .models import GuestReview,PropertyReview

class PropertyReviewSerializer(serializers.ModelSerializer):
    property_slug = serializers.CharField(write_only=True, required=True) 
    user_name = serializers.CharField(source='user.username', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = PropertyReview
        fields = ['id', 'property_slug', 'property_reviewed', 'user_name', 'comment', 'rating', 'parent', 'replies', 'created_at']
        read_only_fields = ['id', 'created_at', 'user_name', 'rating', 'replies', 'property_reviewed']

    def get_replies(self, obj):
        replies = obj.replies.all()
        return ReplySerializer(replies, many=True).data

    def validate_property_slug(self, value):
        try:
            property_instance = Property.objects.get(slug=value)
            return property_instance
        except Property.DoesNotExist:
            raise serializers.ValidationError("Invalid property slug.")

    def create(self, validated_data):
        property_instance = validated_data.pop('property_slug')
        validated_data['property_reviewed'] = property_instance
        parent = validated_data.get('parent')
        if parent is None:
            guest_review_average = GuestReview.objects.filter(property=property_instance).aggregate(
                avg_rating=Avg(
                    (F('staff') + F('facilities') + F('cleanliness') +
                     F('comfort') + F('value_for_money') + F('location') + F('free_wifi')) / 7
                )
            )['avg_rating']
            validated_data['rating'] = guest_review_average or 0

        return PropertyReview.objects.create(user=self.context['request'].user, **validated_data)
    
class ReplySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PropertyReview
        fields = ['id', 'property_reviewed', 'user_name', 'comment', 'replies', 'created_at']
        read_only_fields = ['id', 'property_reviewed', 'user_name', 'created_at', 'replies']

class GuestReviewSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    property_slug = serializers.CharField(write_only=True, required=True)
    user_name = serializers.CharField(source='user.username', read_only=True)  

    class Meta:
        model = GuestReview
        fields = [
            'id', 'user_name', 'property_slug', 'staff', 'facilities', 'cleanliness', 'comfort',
            'value_for_money', 'location', 'free_wifi', 'average_rating', 'created_at'
        ]
        read_only_fields = ['id', 'user_name', 'average_rating', 'category_averages', 'created_at']

    def get_average_rating(self, obj):
        categories = ['staff', 'facilities', 'cleanliness', 'comfort', 'value_for_money', 'location', 'free_wifi']
        values = [getattr(obj, category) for category in categories]
        return sum(values) / len(values)

    def create(self, validated_data):
        property_slug = validated_data.pop('property_slug')
        user = self.context['request'].user  
        try:
            property_instance = Property.objects.get(slug=property_slug)
        except Property.DoesNotExist:
            raise serializers.ValidationError({"property_slug": "Invalid property slug."})

        validated_data['property'] = property_instance
        validated_data['user'] = user 
        return GuestReview.objects.create(**validated_data)
    
class GuestReviewAggregateSerializer(serializers.Serializer):
    property_slug = serializers.CharField()
    average_rating = serializers.FloatField()
    category_averages = serializers.DictField()