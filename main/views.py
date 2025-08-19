from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import (
    Service, BlogPost, Event, Testimonial, 
    TeamMember, Gallery, Contact, ContactMessage, GalleryTag, BlogCategory, ServiceCategory, Technology, FAQ, Portfolio, Newsletter, EventRegistration
)
from .forms import ContactForm, EventRegistrationForm
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class ServiceListView(ListView):
    model = Service
    template_name = 'main/service_list.html'
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_categories'] = ServiceCategory.objects.all()
        context['technologies'] = Technology.objects.all()
        context['faqs'] = FAQ.objects.filter(category='service')
        return context

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'main/service_detail.html'
    context_object_name = 'service'

class BlogListView(ListView):
    model = BlogPost
    template_name = 'main/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True)
        
        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        
        # Search filter
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(meta_description__icontains=search_query)
            )
        
        return queryset.order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        
        # Add active category to context
        category_slug = self.request.GET.get('category')
        if category_slug:
            context['active_category'] = category_slug
            
        return context

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'main/blog_detail.html'
    context_object_name = 'post'

class EventListView(ListView):
    model = Event
    template_name = 'main/event_list.html'
    context_object_name = 'events'
    paginate_by = 9
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset()
        event_type = self.request.GET.get('type')
        if event_type and event_type != 'all':
            queryset = queryset.filter(event_type=event_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_events'] = self.get_queryset().filter(is_upcoming=True)
        context['past_events'] = self.get_queryset().filter(is_upcoming=False)
        context['unique_locations'] = Event.objects.values_list('location', flat=True).distinct()
        context['event_types'] = Event.EVENT_TYPES
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'main/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        
        # Add registration form
        context['form'] = EventRegistrationForm()
        
        # Add related events (same type, excluding current)
        context['related_events'] = Event.objects.filter(
            event_type=event.event_type
        ).exclude(
            id=event.id
        ).order_by('-date')[:3]
        
        return context

class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'main/testimonial_list.html'
    context_object_name = 'testimonials'
    
    def get_queryset(self):
        return Testimonial.objects.all().order_by('-is_featured', 'display_order')

class TeamListView(ListView):
    model = TeamMember
    template_name = 'main/team_list.html'
    context_object_name = 'team_members'
    ordering = ['order']

class GalleryListView(ListView):
    model = Gallery
    template_name = 'main/gallery_list.html'
    context_object_name = 'galleries'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_tags'] = GalleryTag.objects.all()
        return context

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(**form.cleaned_data)
            messages.success(request, 'Thank you for your message. We will get back to you soon!')
            return redirect('main:contact')
    else:
        form = ContactForm()
    
    return render(request, 'main/contact.html', {'form': form})

def contact_success_view(request):
    return render(request, 'main/contact_success.html')

def home_view(request):
    context = {
        'services': Service.objects.all()[:3],
        'recent_posts': BlogPost.objects.filter(is_published=True)[:3],
        'testimonials': Testimonial.objects.filter(is_featured=True)[:3],
        'upcoming_events': Event.objects.filter(is_upcoming=True)[:3]
    }
    return render(request, 'main/home.html', context)

def demo_video_view(request):
    return render(request, 'main/demo_video.html')

class PortfolioListView(ListView):
    model = Portfolio
    template_name = 'main/portfolio_list.html'
    context_object_name = 'portfolios'

@login_required
def dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access the dashboard.")
        return redirect('main:home')
    return render(request, 'main/dashboard.html')

def about_view(request):
    return render(request, 'main/about.html')

def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                Newsletter.objects.get_or_create(email=email)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Thank you for subscribing to our newsletter!'
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': 'An error occurred. Please try again.'
                })
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request'
    })

def event_detail_api(request, pk):
    try:
        event = Event.objects.get(pk=pk)
        data = {
            'title': event.title,
            'description': event.description,
            'date': event.date.strftime('%B %d, %Y'),
            'location': event.location,
            'max_participants': event.max_participants,
            'is_upcoming': event.is_upcoming,
            'price': str(event.price) if event.price else 'Free',
            'highlights': list(event.highlights.values_list('text', flat=True)) if hasattr(event, 'highlights') else []
        }
        return JsonResponse(data)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

def event_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.status = 'pending'
            
            # Check if spots are available
            current_registrations = EventRegistration.objects.filter(event=event).count()
            if event.max_participants and current_registrations >= event.max_participants:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Sorry, this event is fully booked.'
                })
            
            registration.save()
            
            # Send confirmation email
            try:
                # Email to participant
                context = {
                    'name': registration.name,
                    'event': event,
                    'registration': registration,
                }
                html_message = render_to_string('main/email/registration_confirmation.html', context)
                plain_message = strip_tags(html_message)
                
                send_mail(
                    f'Registration Confirmation - {event.title}',
                    plain_message,
                    'noreply@aisolution.com',
                    [registration.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                
                # Email to admin
                admin_html = render_to_string('main/email/admin_notification.html', context)
                admin_plain = strip_tags(admin_html)
                send_mail(
                    f'New Event Registration - {event.title}',
                    admin_plain,
                    'noreply@aisolution.com',
                    ['admin@aisolution.com'],
                    html_message=admin_html,
                    fail_silently=False,
                )
                
            except Exception as e:
                # Log the error but don't prevent registration
                print(f"Email sending failed: {str(e)}")
            
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for registering! Check your email for confirmation.'
            })
        
        return JsonResponse({
            'status': 'error',
            'message': 'Please correct the errors in the form.'
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    })
