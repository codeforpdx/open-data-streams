# Generated by Django 2.1.2 on 2018-11-05 02:26

import cataloger.managers
from django.conf import settings
import django.contrib.auth.validators
import django.contrib.postgres.fields.jsonb
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
            name='Profile',
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
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', cataloger.managers.ProfileManager()),
            ],
        ),
        migrations.CreateModel(
            name='AccessLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accessLevel', models.CharField(default=3, max_length=12)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BureauCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_context', models.URLField(default='https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld')),
                ('_id', models.URLField(default='https://opendatapdx.herokuapp.com/api/')),
                ('_type', models.CharField(default='dcat:Catalog', max_length=12)),
                ('_conformsTo', models.URLField(default='https://project-open-data.cio.gov/v1.1/schema')),
                ('describedBy', models.URLField(default='https://project-open-data.cio.gov/v1.1/schema/catalog.json')),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mtype', models.TextField(default='dcat:Dataset')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('modified', models.DateTimeField(auto_now_add=True)),
                ('identifier', models.URLField()),
                ('rights', models.TextField(blank=True)),
                ('spatial', models.TextField(blank=True)),
                ('temporal', models.TextField(blank=True)),
                ('contactPoint', models.TextField(blank=True)),
                ('describedByType', models.TextField(blank=True)),
                ('describedBy', models.TextField(blank=True)),
                ('accrualPeriodicity', models.TextField(blank=True)),
                ('conformsTo', models.TextField(blank=True)),
                ('dataQuality', models.BooleanField(blank=True, default=False)),
                ('isPartOf', models.TextField(blank=True)),
                ('issued', models.TextField(blank=True)),
                ('landingPage', models.TextField(blank=True)),
                ('primaryITInvestment', models.TextField(blank=True)),
                ('references', models.TextField(blank=True)),
                ('systemOfRecords', models.TextField(blank=True)),
                ('theme', models.TextField(blank=True)),
                ('accessLevel', models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='cataloger.AccessLevel')),
                ('bureauCode', models.ManyToManyField(to='cataloger.BureauCode')),
                ('catalog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cataloger.Catalog')),
            ],
        ),
        migrations.CreateModel(
            name='Distribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mtype', models.TextField(blank=True, default='dcat:Distribution')),
                ('accessURL', models.TextField(blank=True)),
                ('conformsTo', models.TextField(blank=True)),
                ('describedBy', models.TextField(blank=True)),
                ('describedByType', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('downloadURL', models.TextField(blank=True)),
                ('dformat', models.TextField(blank=True)),
                ('mediaType', models.TextField(blank=True)),
                ('title', models.TextField(blank=True)),
                ('dataset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cataloger.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('bureau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cataloger.BureauCode')),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=10)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license', models.CharField(default=3, max_length=12)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('bureau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cataloger.BureauCode')),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cataloger.Division')),
            ],
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.AddField(
            model_name='dataset',
            name='keyword',
            field=models.ManyToManyField(to='cataloger.Keyword'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='language',
            field=models.ManyToManyField(blank=True, default=57, to='cataloger.Language'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='license',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, to='cataloger.License'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='programCode',
            field=models.ManyToManyField(to='cataloger.Division'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dataset',
            name='schema',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cataloger.Schema'),
        ),
        migrations.AddField(
            model_name='profile',
            name='bureau',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cataloger.BureauCode'),
        ),
        migrations.AddField(
            model_name='profile',
            name='division',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cataloger.Division'),
        ),
        migrations.AddField(
            model_name='profile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='profile',
            name='office',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cataloger.Office'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
