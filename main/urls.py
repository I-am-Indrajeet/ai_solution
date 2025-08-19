from django.urls import path
from . import views
from .views import PortfolioListView

app_name = 'main'

urlpatterns = [
    # Home page
    path('', views.home_view, name='home'),
    
    # Services
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    
    # Blog
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    
    # Events
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<int:event_id>/register/', views.event_registration, name='event_registration'),
    
    # Testimonials
    path('testimonials/', views.TestimonialListView.as_view(), name='testimonial_list'),
    
    # Team
    path('team/', views.TeamListView.as_view(), name='team_list'),
    
    # Gallery
    path('gallery/', views.GalleryListView.as_view(), name='gallery_list'),
    
    # Contact
    path('contact/', views.contact_view, name='contact'),
    path('contact/success/', views.contact_success_view, name='contact_success'),
    
    # Demo Video
    path('demo-video/', views.demo_video_view, name='demo_video'),
    
    # Portfolios
    path('portfolios/', PortfolioListView.as_view(), name='portfolio_list'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # About
    path('about/', views.about_view, name='about'),
    
    # Newsletter
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    
    # API
    path('api/events/<int:pk>/', views.event_detail_api, name='event_detail_api'),
]
