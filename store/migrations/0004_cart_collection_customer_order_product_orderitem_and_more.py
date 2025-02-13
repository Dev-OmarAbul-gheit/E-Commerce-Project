# Generated by Django 5.1.4 on 2025-01-30 17:50

import django.core.validators
import django.db.models.deletion
import store.validators
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_user_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('address', models.TextField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__first_name', 'user__last_name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placed_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], default='pending', max_length=15)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.customer')),
            ],
            options={
                'ordering': ['-placed_at'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[store.validators.validate_product_price])),
                ('stock', models.PositiveIntegerField()),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.collection')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='store.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orderitems', to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='store/images/products')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartitems', to='store.product')),
            ],
            options={
                'unique_together': {('product', 'cart')},
            },
        ),
    ]
