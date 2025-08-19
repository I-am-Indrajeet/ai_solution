from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth, TruncDay, ExtractHour
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta
import json
from .models import ContactMessage, BlogPost, Service, Event, EventRegistration

def datetime_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

@staff_member_required
def admin_dashboard(request):
    # Time ranges
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    # Basic Analytics
    message_growth = (
        ContactMessage.objects.filter(created_at__date=today).count() -
        ContactMessage.objects.filter(created_at__date=yesterday).count()
    )

    context = {
        # Today's Stats
        'today_messages': ContactMessage.objects.filter(created_at__date=today).count(),
        'today_events': Event.objects.filter(date__date=today).count(),
        'today_registrations': EventRegistration.objects.filter(registration_date__date=today).count(),
        'today_blogs': BlogPost.objects.filter(published_date__date=today).count(),

        # Growth (compared to yesterday)
        'message_growth': message_growth,
        'message_growth_abs': abs(message_growth),
        
        # Monthly Trends
        'messages_by_month': json.dumps(
            list(ContactMessage.objects.annotate(
                month=TruncMonth('created_at')
            ).values('month').annotate(
                count=Count('id')
            ).order_by('month').values_list('month', 'count')),
            default=datetime_handler
        ),

        # Hourly Distribution
        'messages_by_hour': json.dumps(
            list(ContactMessage.objects.annotate(
                hour=ExtractHour('created_at')
            ).values('hour').annotate(
                count=Count('id')
            ).order_by('hour').values_list('hour', 'count')),
            default=datetime_handler
        ),

        # Category Distribution
        'blog_categories': json.dumps(
            list(BlogPost.objects.values('categories__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]),
            default=datetime_handler
        ),

        # Service Performance
        'service_stats': json.dumps(
            list(Service.objects.values('category__name')
            .annotate(
                count=Count('id'),
            ).order_by('-count')[:10]),
            default=datetime_handler
        ),

        # Event Analytics
        'event_stats': json.dumps(
            list(Event.objects.annotate(
                registration_count=Count('registrations')
            ).values('title', 'registration_count')
            .order_by('-registration_count')[:10]),
            default=datetime_handler
        ),

        # Geographic Distribution (if you have location data)
        'geo_distribution': json.dumps(
            list(EventRegistration.objects.values('event__location')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]),
            default=datetime_handler
        ),

        # Total Counts
        'total_messages': ContactMessage.objects.count(),
        'total_blogs': BlogPost.objects.count(),
        'total_services': Service.objects.count(),
        'total_events': Event.objects.count(),
        'total_registrations': EventRegistration.objects.count(),

        # Jazzmin Integration
        'title': 'Analytics Dashboard',
        'subtitle': 'Comprehensive Site Analytics',
        'is_popup': False,
        'has_permission': True,
        'opts': ContactMessage._meta,
        'app_label': 'main',
    }

    return render(request, 'admin/analytics_dashboard.html', context) 