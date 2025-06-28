from django.contrib import admin
from .models import Facility, Property, Photo, Booking

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    fields = ('image', 'caption', 'order')
    ordering = ('order',)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'responsible',
        'property_type',
        'location',
        'latitude',
        'longitude',
        'guests',
        'bedrooms',
        'is_featured',
        'is_archived',
        'created_at',
    )
    list_filter = ('property_type', 'is_featured', 'is_archived', 'guests')
    search_fields = ('name', 'location')
    inlines = [PhotoInline]
    filter_horizontal = ('facilities',)

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
