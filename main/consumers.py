import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Avg, Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Event, Service, BlogPost, Testimonial, ContactMessage,
    Portfolio, Technology, TeamMember, Gallery
)
import asyncio

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope['user'].is_authenticated or not self.scope['user'].is_staff:
            await self.close()
            return
        await self.accept()
        self.send_updates = True
        self.update_task = asyncio.create_task(self.send_dashboard_data())

    async def disconnect(self, close_code):
        self.send_updates = False
        if self.update_task:
            self.update_task.cancel()

    @database_sync_to_async
    def get_dashboard_data(self):
        now = timezone.now()
        
        # Quick Stats
        total_clients = ContactMessage.objects.values('email').distinct().count()
        upcoming_events = Event.objects.filter(
            date__gte=now.date(),
            is_upcoming=True
        ).order_by('date')
        total_posts = BlogPost.objects.filter(is_published=True).count()
        avg_rating = Testimonial.objects.aggregate(Avg('rating'))['rating__avg'] or 0
        
        # Service Distribution Data
        services = Service.objects.annotate(
            portfolio_count=Count('portfolio'),
            testimonial_count=Count('testimonial')
        )
        
        # Blog Performance Data
        recent_posts = BlogPost.objects.filter(
            is_published=True
        ).order_by('-published_date')[:5]
        
        # Testimonial Distribution
        rating_distribution = [
            Testimonial.objects.filter(rating__lte=1).count(),
            Testimonial.objects.filter(rating__gt=1, rating__lte=2).count(),
            Testimonial.objects.filter(rating__gt=2, rating__lte=3).count(),
            Testimonial.objects.filter(rating__gt=3, rating__lte=4).count(),
            Testimonial.objects.filter(rating__gt=4).count(),
        ]
        
        # Recent Activities
        activities = []
        
        # Add recent blog posts
        for post in BlogPost.objects.order_by('-created_date')[:3]:
            activities.append({
                'date': post.created_date.strftime('%Y-%m-%d %H:%M'),
                'type': 'Blog Post',
                'description': post.title,
                'status': 'Published' if post.is_published else 'Draft',
                'status_color': 'success' if post.is_published else 'warning'
            })
        
        # Add recent events
        for event in Event.objects.order_by('-date')[:3]:
            activities.append({
                'date': event.date.strftime('%Y-%m-d %H:%M'),
                'type': 'Event',
                'description': event.title,
                'status': 'Upcoming' if event.is_upcoming else 'Past',
                'status_color': 'primary' if event.is_upcoming else 'secondary'
            })
        
        # Add recent testimonials
        for testimonial in Testimonial.objects.order_by('-id')[:3]:
            activities.append({
                'date': timezone.now().strftime('%Y-%m-%d %H:%M'),
                'type': 'Testimonial',
                'description': f"New review from {testimonial.client_name}",
                'status': f"{testimonial.rating}★",
                'status_color': 'warning'
            })
        
        # Sort activities by date
        activities.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M'), reverse=True)
        activities = activities[:5]  # Keep only the 5 most recent

        data = {
            'total_clients': total_clients,
            'upcoming_events': upcoming_events.count(),
            'total_posts': total_posts,
            'avg_rating': round(avg_rating, 1),
            
            'stats_details': {
                'total_ratings': Testimonial.objects.count(),
                'avg_read_time': round(BlogPost.objects.filter(is_published=True).aggregate(Avg('read_time'))['read_time__avg'] or 0, 1),
                'next_events': [
                    {
                        'title': event.title,
                        'date': event.date.strftime('%Y-%m-%d %H:%M'),
                        'location': event.location,
                        'event_type': event.get_event_type_display()
                    }
                    for event in upcoming_events[:5]
                ],
                'unique_companies': ContactMessage.objects.values('company_name').distinct().count()
            },
            
            'services_data': {
                'labels': [service.title for service in services],
                'values': [service.portfolio_count + service.testimonial_count for service in services]
            },
            
            'blog_data': {
                'labels': [post.title[:30] + '...' if len(post.title) > 30 else post.title 
                          for post in recent_posts],
                'values': [post.read_time for post in recent_posts]
            },
            
            'ratings_data': {
                'values': rating_distribution
            },
            
            'recent_activity': activities
        }
        
        return data

    async def send_dashboard_data(self):
        while self.send_updates:
            try:
                data = await self.get_dashboard_data()
                await self.send(text_data=json.dumps(data))
                await asyncio.sleep(10)  # Update every 10 seconds
            except Exception as e:
                print(f"Error in send_dashboard_data: {e}")
                await asyncio.sleep(5) 