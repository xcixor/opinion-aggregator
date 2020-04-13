# Generated by Django 2.0.2 on 2020-04-13 11:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(error_messages={'unique': 'The email address you entered has already been registered.'}, max_length=255, unique=True, verbose_name='email address')),
                ('firstname', models.CharField(blank=True, max_length=40, verbose_name='firstname')),
                ('lastname', models.CharField(blank=True, max_length=40, verbose_name='lastname')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='address')),
                ('gender', models.CharField(blank=True, max_length=40, verbose_name='gender')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date_joined')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='date_of_birth')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_change_allowed', models.BooleanField(default=False, help_text='Designates whether this user has been authorized to change his own password, in the change_password view.', verbose_name='change_allowed')),
                ('phone_number', models.IntegerField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('change_email', models.EmailField(blank=True, default=None, error_messages={'unique': 'The email address you entered has already been registered.'}, max_length=255, null=True, unique=True, verbose_name='email address')),
                ('former_email', models.EmailField(blank=True, default=None, max_length=255, null=True, verbose_name='email address')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CountryCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.IntegerField(default=971, unique=True)),
                ('country', models.CharField(default='UAE', max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='country_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='opinion_aggregator.CountryCode'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
