from django.contrib import admin
from django.utils.html import format_html
from .models import Document, Verification

@admin.action(description="Mark selected documents as Verified")
def mark_documents_verified(modeladmin, request, queryset):
    queryset.update(is_verified=True)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_by', 'document_type', 'uploaded_at', 'is_verified', 'preview_file')
    list_filter = ('document_type', 'is_verified', 'uploaded_at')
    search_fields = ('uploaded_by__username',)
    readonly_fields = ('uploaded_at', 'preview_file')
    actions = [mark_documents_verified]

    def preview_file(self, obj):
        if obj.file:
            if obj.file.name.endswith('.pdf'):
                return format_html(f"<a href='{obj.file.url}' target='_blank'>View PDF</a>")
            elif obj.file.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                return format_html(f"<img src='{obj.file.url}' width='100' height='100' />")
        return "No Preview"
    preview_file.short_description = "File Preview" 

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs
        return qs.filter(is_verified=True)

@admin.action(description="Mark selected verifications as Verified")
def mark_verified(modeladmin, request, queryset):
    queryset.update(is_verified=True)

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'verification_type', 'target_user', 'target_property', 'is_verified', 'verified_at')
    list_filter = ('verification_type', 'is_verified', 'verified_at')
    search_fields = ('target_user__username', 'target_property__location')
    readonly_fields = ('verified_at',)
    actions = [mark_verified]
