# Generated by Django 4.2.7 on 2023-11-05 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_vocabularyword_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='vocabularyword',
            name='group_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='vocabularyword',
            name='user',
            field=models.ForeignKey(default=None, blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]