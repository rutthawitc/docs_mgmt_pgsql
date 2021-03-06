# Generated by Django 3.0.6 on 2020-05-15 12:26

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
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_count', models.IntegerField()),
                ('doc_mtno', models.CharField(max_length=50)),
                ('doc_title', models.CharField(max_length=150)),
                ('doc_desc', models.CharField(max_length=150)),
                ('doc_date', models.DateField(blank=True, null=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RefDocumentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_code', models.CharField(max_length=10)),
                ('type_desc', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='UserDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_code', models.CharField(max_length=35)),
                ('department_title', models.CharField(max_length=150)),
                ('department_desc', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='UserSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_code', models.CharField(max_length=35)),
                ('section_title', models.CharField(max_length=150)),
                ('section_desc', models.CharField(max_length=150)),
                ('department_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docsmgmt.UserDepartment')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('employee_id', models.CharField(max_length=12)),
                ('dept', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='docsmgmt.UserDepartment')),
                ('sect', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='docsmgmt.UserSection')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentSections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_title', models.CharField(max_length=100)),
                ('section_sequence', models.IntegerField()),
                ('section_desc', models.CharField(max_length=200)),
                ('doc_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docsmgmt.Documents')),
            ],
        ),
        migrations.AddField(
            model_name='documents',
            name='type_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docsmgmt.RefDocumentType'),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True)),
                ('comment_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('doc_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docsmgmt.Documents')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docsmgmt.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Accepted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.BooleanField(default=False)),
                ('doc_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docsmgmt.Documents')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docsmgmt.UserProfile')),
            ],
        ),
    ]
