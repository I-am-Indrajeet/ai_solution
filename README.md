# AI Solution Platform

A feature-rich Django web application for managing services, blogs, events, testimonials, team, gallery, portfolios, and more, with a modern admin dashboard and real-time analytics.
![Alt text](https://github.com/I-am-Indrajeet/ai_solution/blob/34237bd5b0be37d5c8dd05b4ab38518308e63af4/Screenshot%202025-01-02%20221501.png)


## Features

- **Service Management**: Categorize and display services with icons, images, and features.
- **Blog System**: Publish, categorize, and tag blog posts with SEO support.
- **Event Management**: List, register, and analyze events with participant tracking.
- **Testimonials**: Collect and showcase client testimonials with ratings.
- **Team & Portfolio**: Present team members and project portfolios.
- **Gallery**: Manage and tag image galleries.
- **Contact & Newsletter**: Contact form with message storage and newsletter signup.
- **Admin Dashboard**: Custom analytics dashboard with charts and stats (Jazzmin theme).
- **Real-time Analytics**: WebSocket-powered dashboard for live updates (Django Channels).
- **Custom Template Filters**: For advanced template logic.
- **Responsive Frontend**: Bootstrap-based templates.

## Project Structure

- `ai_solution/` – Django project settings and root URLs.
- `main/` – Main app with models, views, admin, forms, consumers, and templates.
- `media/` – Uploaded images and files.
- `static/` – Static files (CSS, JS, images).

## Requirements

- Python 3.8+
- Django 5.1.x
- django-channels
- django-jazzmin
- (Other dependencies: see below)

### Python Dependencies

Since there is no `requirements.txt`, here are the main packages you need:

```txt
Django>=5.1,<6.0
channels
jazzmin
Pillow
```

You may also need:
- djangorestframework (if you want to extend with APIs)
- Any other package you use for email or additional features

Install with:

```bash
pip install Django channels jazzmin Pillow
```

## Setup Instructions

1. **Clone the repository** and navigate to the project root.

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    Or, if `requirements.txt` is missing, use the list above.

3. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

4. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

5. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

6. **Access the site**:
    - Main site: http://127.0.0.1:8000/
    - Admin: http://127.0.0.1:8000/admin/

## Admin Dashboard

- Custom analytics dashboard at `/admin/dashboard/`
- Uses Jazzmin for a modern admin UI
- Real-time updates via Django Channels (WebSocket)

## Customization

- **Email**: Configure your SMTP settings in `ai_solution/settings.py` for contact and registration emails.
- **Media/Static**: Place your images and static files in the respective folders.
- **Templates**: Edit HTML files in `main/templates/main/` for frontend customization.

## Testing

- Basic test structure is present in `main/tests.py`. Extend with your own tests as needed.
- Run tests with:
    ```bash
    python manage.py test
    ```

## Project Apps and Key Files

- `main/models.py`: All core data models (Service, BlogPost, Event, Testimonial, etc.)
- `main/views.py`: Main business logic and page views.
- `main/consumers.py`: WebSocket consumers for real-time dashboard.
- `main/admin_views.py`: Custom admin dashboard logic.
- `main/forms.py`: Contact and event registration forms.
- `main/urls.py`: App URL routing.
- `main/admin.py`: Django admin customizations.
- `main/templatetags/custom_filters.py`: Custom template filters.

## Real-time Features

- WebSocket endpoint: `ws/dashboard/`
- Live dashboard updates for staff users.

## License

[MIT] or your chosen license. 
