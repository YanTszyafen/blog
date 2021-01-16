# Generated by Django 2.2 on 2021-01-16 11:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Category management',
                'verbose_name_plural': 'Category management',
                'db_table': 'tb_category',
            },
        ),
    ]
