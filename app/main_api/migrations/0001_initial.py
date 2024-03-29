# Generated by Django 3.2.5 on 2021-07-21 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('probability', models.PositiveSmallIntegerField()),
                ('insurance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coupons', to='main_api.insurance')),
            ],
        ),
        migrations.CreateModel(
            name='UserCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('insurance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_coupons', to='main_api.insurance')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insurance_coupons', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'insurance')},
            },
        ),
    ]
