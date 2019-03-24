# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-12-15 20:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_auto_20181215_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_price',
            field=models.IntegerField(default=500000),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='addons',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='agentinfo',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='conversations',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.UserInfo'),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='addons',
            field=models.ManyToManyField(blank=True, null=True, related_name='choosed_addons', to='chat.Addons'),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='insurance_type',
            field=models.ManyToManyField(blank=True, null=True, related_name='insurance_type', to='chat.InsuranceType'),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.UserInfo'),
        ),
        migrations.AlterField(
            model_name='insurancetype',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.AgentInfo'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='insurance',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.Insurance'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='purpose',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.UserInfo'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='fb_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='addons',
            field=models.ManyToManyField(blank=True, null=True, related_name='available_addons', to='chat.Addons'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.Company'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='model_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
