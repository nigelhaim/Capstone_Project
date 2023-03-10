# Generated by Django 4.1.5 on 2023-01-13 12:56

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
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
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='proj_files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='./files/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('description', models.CharField(max_length=500)),
                ('profession', models.CharField(max_length=50)),
                ('Highest_edu_attain', models.CharField(default='', max_length=75)),
                ('contact_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('datePosted', models.DateTimeField()),
                ('thread_files', models.ManyToManyField(blank=True, related_name='t_proj_files', to='idasia.proj_files')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='t_profile', to='idasia.profile')),
            ],
        ),
        migrations.AddField(
            model_name='proj_files',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='u_profile', to='idasia.profile'),
        ),
        migrations.CreateModel(
            name='idea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proj_title', models.CharField(default='', max_length=50)),
                ('proj_content', models.CharField(max_length=500)),
                ('dateCreated', models.DateTimeField()),
                ('proj_objective', models.CharField(max_length=1000)),
                ('proj_location', models.CharField(max_length=30)),
                ('proj_background', models.CharField(max_length=1000)),
                ('proj_status', models.CharField(max_length=20)),
                ('proj_image', models.CharField(default='', max_length=800)),
                ('proj_cost', models.IntegerField()),
                ('proj_category', models.ManyToManyField(blank=True, related_name='i_category', to='idasia.category')),
                ('thread', models.ManyToManyField(blank=True, related_name='thread', to='idasia.thread')),
                ('proj_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='i_profile', to='idasia.profile')),
                ('proj_coAuthor', models.ManyToManyField(blank=True, related_name='Co_Author', to='idasia.profile')),
                ('proj_collaborator', models.ManyToManyField(blank=True, related_name='collaborator', to='idasia.profile')),
            ],
        ),
    ]
