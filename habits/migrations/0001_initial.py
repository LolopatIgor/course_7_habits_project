# Generated by Django 5.1.2 on 2024-12-07 11:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=255)),
                ('time', models.TimeField()),
                ('action', models.TextField()),
                ('is_pleasant', models.BooleanField(default=False)),
                ('period_days', models.PositiveIntegerField(default=1)),
                ('reward', models.CharField(blank=True, max_length=255, null=True)),
                ('duration_seconds', models.PositiveIntegerField()),
                ('is_public', models.BooleanField(default=False)),
                ('linked_habit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='habits.habit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habits', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]