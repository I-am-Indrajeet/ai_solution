from django import template
import calendar

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return '' 

@register.filter
def month_name(month_number):
    try:
        return calendar.month_name[int(month_number)]
    except (ValueError, IndexError):
        return '' 

@register.filter
def absolute(value):
    return abs(value)

@register.filter
def filter_events(events, event_type):
    """Filter events by event type"""
    if not events:
        return []
    return [event for event in events if event.event_type == event_type] 