from rest_framework import serializers
from .models import PropertyFAQ, MoreLivingFAQ

class ReplySerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    posted_at = serializers.DateTimeField(source='created_at', format="%d %b %Y", read_only=True)

    class Meta:
        model = PropertyFAQ
        fields = ['id', 'user_name', 'question_text', 'posted_at']

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}" if obj.user else "Unknown"


class PropertyFAQSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    posted_at = serializers.DateTimeField(source='created_at', format="%d %b %Y", read_only=True)
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = PropertyFAQ
        fields = ['id', 'full_name', 'question_text', 'posted_at', 'replies']
        read_only_fields = ['id', 'user', 'property', 'replies']

    def get_full_name(self, obj):
        user = obj.user
        return f"{user.first_name} {user.last_name}" if user else "Unknown"


class WebsiteFAQSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    posted_at = serializers.DateTimeField(source='created_at', format="%d %b %Y", read_only=True)
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = MoreLivingFAQ
        fields = ['id', 'full_name', 'question_text', 'posted_at', 'replies']
        read_only_fields = ['id', 'user', 'replies']

    def get_full_name(self, obj):
        user = obj.user
        return f"{user.first_name} {user.last_name}" if user else "Unknown"