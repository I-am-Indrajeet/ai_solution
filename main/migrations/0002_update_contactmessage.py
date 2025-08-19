from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='subject',
            field=models.CharField(max_length=200, default='No Subject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ] 