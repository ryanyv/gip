from django.contrib import admin
from django.utils.html import format_html
from .models import Facility, Property, Photo, Booking

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    fields = ('image', 'caption', 'order')
    ordering = ('order',)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    change_list_template = "admin/properties/property/change_list.html"
    list_display = (
        'thumbnail',
        'name',
        'responsible',
        'property_type',
        'location',
        'latitude',
        'longitude',
        'guests',
        'bedrooms',
        'is_featured',
        'created_at',
    )
    list_display_links = None
    list_filter = ('property_type', 'is_featured', 'guests')
    search_fields = ('name', 'location')
    inlines = [PhotoInline]
    filter_horizontal = ('facilities',)

    @admin.display(description="Photo")
    def thumbnail(self, obj):
        first_photo = obj.photos.first()
        if first_photo:
            return format_html(
                '<img src="{}" width="60" height="45" style="object-fit:cover;"/>',
                first_photo.image.url,
            )
        return ""

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('property', 'order', 'caption')
    list_filter = ('property',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('property', 'status', 'start_date', 'end_date')
    search_fields = ('property__name', 'user__username')
