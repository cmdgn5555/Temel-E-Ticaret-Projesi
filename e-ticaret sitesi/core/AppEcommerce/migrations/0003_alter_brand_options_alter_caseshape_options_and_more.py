# Generated by Django 5.0.8 on 2024-11-04 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppEcommerce', '0002_brand_brand_en_brand_brand_tr_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name_plural': 'Markalar'},
        ),
        migrations.AlterModelOptions(
            name='caseshape',
            options={'verbose_name_plural': 'Kasa Şekilleri'},
        ),
        migrations.AlterModelOptions(
            name='color',
            options={'verbose_name_plural': 'Renkler'},
        ),
        migrations.AlterModelOptions(
            name='gender',
            options={'verbose_name_plural': 'Cinsiyetler'},
        ),
        migrations.AlterModelOptions(
            name='glassfeature',
            options={'verbose_name_plural': 'Cam Özellikleri'},
        ),
        migrations.AlterModelOptions(
            name='mechanism',
            options={'verbose_name_plural': 'Mekanizmalar'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Ürünler'},
        ),
        migrations.AlterModelOptions(
            name='straptype',
            options={'verbose_name_plural': 'Kayış Tipleri'},
        ),
        migrations.AlterModelOptions(
            name='style',
            options={'verbose_name_plural': 'Tarzlar'},
        ),
    ]
