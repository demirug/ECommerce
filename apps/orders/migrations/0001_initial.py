# Generated by Django 4.1 on 2022-08-18 23:21

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('status', models.CharField(choices=[('NEW', 'NEWm'), ('PAYED', 'PAYED'), ('DONE', 'Done'), ('CANCELED', 'CANCELED')], default='NEW', max_length=15, verbose_name='Status')),
                ('cost', models.DecimalField(decimal_places=1, max_digits=5, verbose_name='Cost')),
                ('first_name', models.CharField(max_length=100, verbose_name='First name')),
                ('second_name', models.CharField(max_length=100, verbose_name='Second name')),
                ('last_name', models.CharField(max_length=100, verbose_name='Last name')),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed", regex='^\\+?1?\\d{9,15}$')])),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='products.product')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
            ],
            options={
                'verbose_name': 'OrderItem',
                'verbose_name_plural': 'OrderItems',
            },
        ),
    ]
