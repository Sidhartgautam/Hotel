from rest_framework import serializers
from django.db.models import Avg,F
from django.db import models
from .models import GuestReview,PropertyReview

class PropertyReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = PropertyReview
        fields = ['id', 'property_reviewed', 'user_name', 'comment', 'rating', 'parent', 'replies', 'created_at']
        read_only_fields = ['id', 'created_at', 'user_name', 'rating', 'replies']

    def get_replies(self, obj):
        replies = obj.replies.all()
        return ReplySerializer(replies, many=True).data
    
    def validate(self, data):
        parent = data.get('parent')
        if parent:
            property_owner = parent.property_reviewed.user.is_hotel_owner
            request_user = self.context['request'].user

            if property_owner != request_user:
                raise serializers.ValidationError("Only the property owner can reply to this review.")

        return data


    def validate_rating(self, value):
        if value >= 10:
            raise serializers.ValidationError("Rating must be less than 10.")
        return value

    def create(self, validated_data):
        parent = validated_data.get('parent')
        if parent is None:
            property_reviewed = validated_data['property_reviewed']
            guest_review_average = GuestReview.objects.filter(property=property_reviewed).aggregate(
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
    category_averages = serializers.SerializerMethodField()

    class Meta:
        model = GuestReview
        fields = [
            'id', 'property', 'staff', 'facilities', 'cleanliness', 'comfort',
            'value_for_money', 'location', 'free_wifi', 'average_rating', 'category_averages', 'created_at'
        ]
        read_only_fields = ['id', 'average_rating', 'category_averages', 'created_at']

    def get_average_rating(self, obj):
        # Compute the average of all categories for a single review
        categories = ['staff', 'facilities', 'cleanliness', 'comfort', 'value_for_money', 'location', 'free_wifi']
        values = [getattr(obj, category) for category in categories]
        return sum(values) / len(values)

    def get_category_averages(self, obj):
    # Retrieve all existing reviews for the property, including the current one
        reviews = GuestReview.objects.filter(property=obj.property)
        category_fields = ['staff', 'facilities', 'cleanliness', 'comfort', 'value_for_money', 'location', 'free_wifi']

        # If there are no other reviews, return the current review's values
        if reviews.count() == 1:  # This means only the current review exists
            return {field: getattr(obj, field) for field in category_fields}

        # Otherwise, calculate the average across all reviews
        averages = {}
        for field in category_fields:
            avg_value = reviews.aggregate(avg=models.Avg(field)).get(f'{field}__avg')
            averages[field] = avg_value if avg_value is not None else 0

        return averages