# Generated by Django 4.2.7 on 2023-11-12 03:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_remove_vocabularyword_group_name_groupname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupname',
            name='group_name',
            field=models.CharField(blank=True, default='Others', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='groupname',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]