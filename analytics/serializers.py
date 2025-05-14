from rest_framework import serializers
from .models import PropertyView, SearchQuery, Feedback

class PropertyViewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    property = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = PropertyView
        fields = ['id', 'user', 'property', 'viewed_at']

class SearchQuerySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SearchQuery
        fields = ['id', 'user', 'query_text', 'timestamp']

class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    property = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'feedback_type', 'property', 'message', 'submitted_at']
