# Generated by Django 2.2.13 on 2021-07-04 07:51

import common.validators
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('en_name', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z\\s]+$')])),
                ('fa_name', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[\u0600-ۿ\\s]+$')])),
                ('phone', models.CharField(max_length=11, null=True, unique=True, validators=[common.validators.mobile_validator, common.validators.mobile_length_validator])),
                ('verify_phone', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('file_resume', models.FileField(null=True, upload_to='media/resume/')),
                ('code', models.FileField(null=True, upload_to='media/code/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('team', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uteam', to='accounts.Team')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TeamUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^[\u0600-ۿ\\s]+$')])),
                ('last_name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^[\u0600-ۿ\\s]+$')])),
                ('file_resume', models.FileField(upload_to='media/resume')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mteam', to='accounts.Team')),
            ],
            options={
                'unique_together': {('team', 'first_name', 'last_name')},
            },
        ),
    ]
