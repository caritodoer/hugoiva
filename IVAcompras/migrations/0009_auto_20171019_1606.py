# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-19 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IVAcompras', '0008_auto_20171019_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle',
            name='gravado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True, verbose_name='Gravado'),
        ),
        migrations.AlterField(
            model_name='detalle',
            name='imp_int',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True, verbose_name='Imp. Internos'),
        ),
        migrations.AlterField(
            model_name='detalle',
            name='iva105',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True, verbose_name='I.V.A. 10,5%'),
        ),
        migrations.AlterField(
            model_name='detalle',
            name='iva21',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True, verbose_name='I.V.A. 21%'),
        ),
        migrations.AlterField(
            model_name='detalle',
            name='iva_otros',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True, verbose_name='Otros I.V.A.'),
        ),
        migrations.AlterField(
            model_name='detalle',
            name='no_gravado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True, verbose_name='No Gravado'),
        ),
        migrations.AlterField(
            model_name='detalle',
            name='otros',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True, verbose_name='Otros'),
        ),
        migrations.AlterField(
            model_name='detalle',
            name='ret_IVA',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True, verbose_name='Ret. I.V.A.'),
        ),
        migrations.AlterField(
            model_name='detalle',
            name='ret_iibb',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True, verbose_name='Ret. IIBB'),
        ),
        migrations.AlterField(
            model_name='detalle',
            name='rg2126',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True, verbose_name='R.G. 2126'),
        ),
    ]