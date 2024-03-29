# Generated by Django 5.0.1 on 2024-02-07 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('base_currency', models.CharField(max_length=15)),
                ('quote_currency', models.CharField(max_length=15)),
                ('max_orders_per_minute', models.PositiveSmallIntegerField()),
                ('min_order_amount_value', models.DecimalField(decimal_places=10, max_digits=22)),
                ('min_order_amount_currency', models.CharField(max_length=15)),
                ('taker_fee', models.DecimalField(decimal_places=10, max_digits=22)),
                ('taker_discount_percentage', models.DecimalField(decimal_places=10, max_digits=22)),
                ('maker_fee', models.DecimalField(decimal_places=10, max_digits=22)),
                ('maker_discount_percentage', models.DecimalField(decimal_places=10, max_digits=22)),
            ],
            options={
                'managed': False,
            },
        ),
    ]
