from django.contrib import admin
from .models import Event, Participant, Resource, Sweet, Sale, DiwaliWish, Diya, Question, UserDiwaliInfo,DiwaliCelebration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'date')

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'event','region')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'category', 'quantity')

@admin.register(UserDiwaliInfo)
class UserDiwaliInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'region', 'special_sweets')


@admin.register(DiwaliCelebration)
class DiwaliCelebrationAdmin(admin.ModelAdmin):
    list_display = ('region', 'special_sweets', 'celebration_description')  # Display columns
    search_fields = ('region', 'special_sweets')  # Search functionality
    list_filter = ('region',)  # Filter options

@admin.register(Sweet)
class SweetAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('name', 'price', 'stock', 'image_preview')

    # Search functionality for the list view
    search_fields = ('name',)

    # Fields to filter by in the admin interface
    list_filter = ('price', 'stock')

    # Allows the image field to be displayed as a preview in the list
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" />'
        return 'No image'
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'

    # Define the fields to display in the admin form
    # Instead of using both 'fields' and 'fieldsets', we will use 'fieldsets'
    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'stock', 'image')
        }),
    )

    # Auto-populate the image URL in the admin interface
    readonly_fields = ('image_preview',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('sweet', 'quantity', 'sale_date')

@admin.register(DiwaliWish)
class WishAdmin(admin.ModelAdmin):
    list_display = ('name', 'favorite_sweet', 'wish', 'created_at')  # Ensure valid fields
    search_fields = ('name', 'favorite_sweet')  # Optional: Add a search bar

@admin.register(Diya)
class DiyaAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'status')  # Display the columns in the admin list view
    list_filter = ('status',)  # Allows filtering of diyas by their status (lit/unlit)
    search_fields = ('latitude', 'longitude')  # Allows searching diyas by coordinates

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'correct_answer')
