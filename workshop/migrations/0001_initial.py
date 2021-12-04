# Generated by Django 3.2.8 on 2021-11-17 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Workshop name')),
                ('description', models.TextField(verbose_name='Description')),
                ('city', models.CharField(blank=True, max_length=120, null=True, verbose_name='City')),
                ('zip_code', models.CharField(blank=True, max_length=15, null=True, verbose_name='Zip code')),
                ('street', models.CharField(blank=True, max_length=150, null=True, verbose_name='Street')),
                ('image', models.TextField()),
                ('phone_number', models.CharField(blank=True, max_length=25, null=True, verbose_name='Phone number')),
                ('page', models.URLField(verbose_name='Page url')),
                ('is_active', models.BooleanField()),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.workshopowner')),
            ],
        ),
        migrations.CreateModel(
            name='ServicesPriceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Service name')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Service price')),
                ('workshop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='workshop.workshop')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_hour', models.TimeField()),
                ('to_hour', models.TimeField()),
                ('day_of_week', models.CharField(choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')], max_length=20, verbose_name='Day of week')),
                ('is_open', models.BooleanField()),
                ('workshop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='workshop.workshop')),
            ],
        ),
        migrations.AddConstraint(
            model_name='businesshours',
            constraint=models.UniqueConstraint(fields=('workshop', 'day_of_week'), name='unique_days'),
        ),
    ]
