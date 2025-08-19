from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    color_class = models.CharField(max_length=50, default='blue')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Service Categories'
        ordering = ['order']

    def __str__(self):
        return self.name

class Service(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    icon = models.ImageField(upload_to='services/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    short_description = models.CharField(max_length=200, help_text="Brief description for cards")
    features = models.JSONField(null=True, blank=True, help_text="List of service features")
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='blog/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField('BlogCategory')
    is_published = models.BooleanField(default=False)
    tags = models.ManyToManyField('BlogTag', blank=True)
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description")
    read_time = models.PositiveIntegerField(help_text="Estimated reading time in minutes", default=5)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Blog Categories"

class Event(models.Model):
    EVENT_TYPES = [
        ('all', 'All Events'),
        ('workshop', 'Workshop'),
        ('conference', 'Conference'),
        ('webinar', 'Webinar'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    featured_image = models.ImageField(upload_to='events/', null=True, blank=True)
    is_upcoming = models.BooleanField(default=True)
    end_date = models.DateTimeField(null=True, blank=True)
    registration_url = models.URLField(blank=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='all')
    
    def __str__(self):
        return self.title

    @property
    def is_past(self):
        return timezone.now() > self.date

class EventPhoto(models.Model):
    event = models.ForeignKey(Event, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_photos/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo from {self.event.title}"

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    content = models.TextField()
    client_photo = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Rating from 0 to 5"
    )
    is_featured = models.BooleanField(default=False)
    client_position = models.CharField(max_length=100, blank=True)
    display_order = models.IntegerField(default=0)
    project_name = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"Testimonial from {self.client_name}"

    class Meta:
        ordering = ['-is_featured', 'display_order']

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='team/', null=True, blank=True)
    email = models.EmailField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name 

class Navigation(models.Model):
    """Model for navigation menu items"""
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)  # For dropdown menus
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Navigation Items"

class BlogTag(models.Model):
    """Model for blog tags"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/', help_text="Image for the gallery",default=timezone.now)
    description = models.TextField(blank=True)
    alt_text = models.CharField(max_length=200, help_text="Alternative text for accessibility")
    tags = models.ManyToManyField('GalleryTag', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "Galleries"
        ordering = ['-created_at']

    def __str__(self):
        return f"Gallery Image {self.id}"

class GalleryTag(models.Model):
    """Model for gallery tags"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

class Contact(models.Model):
    subject = models.CharField(max_length=200)
    preferred_contact_method = models.CharField(
        max_length=20,
        choices=[
            ('EMAIL', 'Email'),
            ('PHONE', 'Phone'),
            ('EITHER', 'Either')
        ],
        default='EMAIL'
    )
    best_time_to_contact = models.CharField(max_length=100, blank=True)
    attachment = models.FileField(upload_to='contact_attachments/', blank=True, null=True) 

class Technology(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='technologies/')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Technologies'
        ordering = ['order']

    def __str__(self):
        return self.name

class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('service', 'Service'),
        ('product', 'Product'),
        ('general', 'General'),
    ]
    
    question = models.CharField(max_length=200)
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['order']

    def __str__(self):
        return self.question 

class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    features = models.JSONField(help_text="List of key features")
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='portfolios/', null=True, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Portfolios"

    def __str__(self):
        return self.title 

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-subscribed_at'] 

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='pending')

    def __str__(self):
        return f"{self.name} - {self.event.title}"

    class Meta:
        ordering = ['-registration_date'] 