from django.contrib import admin
from .models import PropertyView, SearchQuery, Feedback

@admin.register(PropertyView)
class PropertyViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'property', 'viewed_at')
    search_fields = ('user__username', 'property__location')
    list_filter = ('viewed_at',)


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'query_text', 'timestamp')
    search_fields = ('user__username', 'query_text')
    list_filter = ('timestamp',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'feedback_type', 'property', 'submitted_at')
    search_fields = ('user__username', 'message')
    list_filter = ('feedback_type', 'submitted_at')

