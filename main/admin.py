from django.contrib import admin
from .models import (
    Service, BlogPost, Event, Testimonial, 
    TeamMember, Gallery, Contact, ContactMessage, 
    GalleryTag, BlogCategory, ServiceCategory, 
    Technology, FAQ, Portfolio, Newsletter, 
    EventRegistration, BlogTag, Navigation
)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company_name', 'job_title')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'updated_date')
    search_fields = ('title', 'description')
    list_filter = ('created_date',)
    date_hierarchy = 'created_date'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published', 'read_time')
    list_filter = ('is_published', 'categories', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'published_date'
    filter_horizontal = ('categories', 'tags')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_upcoming', 'event_type')
    list_filter = ('is_upcoming', 'event_type', 'date')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company', 'rating', 'is_featured')
    list_filter = ('is_featured', 'rating')
    search_fields = ('client_name', 'company', 'content')
    ordering = ('-is_featured', 'display_order')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'email', 'order')
    search_fields = ('name', 'position', 'bio')
    list_filter = ('position',)
    ordering = ('order',)

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'alt_text', 'created_at')
    list_filter = ('tags', 'created_at')
    search_fields = ('description', 'alt_text')
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'

@admin.register(Navigation)
class NavigationAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'order', 'is_active', 'parent')
    list_filter = ('is_active',)
    search_fields = ('title', 'url')
    ordering = ('order',)

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(GalleryTag)
class GalleryTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'color_class', 'order')
    list_filter = ('color_class',)
    search_fields = ('name',)
    ordering = ('order',)

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name',)
    ordering = ('order',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('question', 'answer')
    ordering = ('order',)

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'order')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_date'
    ordering = ('order',)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    date_hierarchy = 'subscribed_at'

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event', 'registration_date', 'status')
    list_filter = ('status', 'registration_date', 'event')
    search_fields = ('name', 'email', 'phone')
    date_hierarchy = 'registration_date'
