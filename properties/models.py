from django.db import models
from django.conf import settings

PROPERTY_TYPE_CHOICES = [
    ('short-term', 'Short-Term Rental'),
    ('long-term', 'Long-Term Rental'),
    ('investment', 'Investment Project'),
]

class Facility(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Property(models.Model):
    name = models.CharField(max_length=255)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    location = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255, blank=True)
    guests = models.PositiveIntegerField(default=1)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    area = models.PositiveIntegerField(help_text="Area in square meters", blank=True, null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    video = models.FileField(upload_to='property_videos/', blank=True, null=True)
    # Geographic coordinates (optional – enable future map integration)
    latitude = models.FloatField(
        blank=True,
        null=True,
        help_text="Latitude in decimal degrees",
    )
    longitude = models.FloatField(
        blank=True,
        null=True,
        help_text="Longitude in decimal degrees",
    )
    facilities = models.ManyToManyField(Facility, related_name='properties', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="responsible_properties",
    )

    class Meta:
        permissions = [
            ("assign_responsible", "Can assign responsible user to property"),
        ]

    def __str__(self):
        return self.name

class Photo(models.Model):
    property = models.ForeignKey(Property, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_photos/')
    order = models.PositiveIntegerField(default=0)
    caption = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.property.name} Photo #{self.order}"

class Booking(models.Model):
    property = models.ForeignKey(Property, related_name='bookings', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='booked')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property.name}: {self.start_date} → {self.end_date}"
