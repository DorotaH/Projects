# Generated by Django 4.2.7 on 2024-03-03 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listing_watchlist_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.URLField(default='https://t3.ftcdn.net/jpg/03/08/79/70/360_F_308797039_9fsJmkRwEcLJT73bk0EbGIqKpQiibfVa.jpg'),
        ),
    ]