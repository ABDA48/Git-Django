# Generated by Django 3.2.3 on 2024-09-24 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20240910_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepotLivre',
            fields=[
                ('reference', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('designation', models.CharField(blank=True, max_length=100)),
                ('category', models.CharField(choices=[('Quran', 'Quran'), ('Fiqh', 'Fiqh'), ('Anqaeed', 'Anqaeed'), ('Douan', 'Douan'), ('Sirat', 'Sirat'), ('Akhlaq', 'Akhlaq')], default='Quran', max_length=100)),
                ('language', models.CharField(choices=[('Mg', 'Mg'), ('Ar', 'Ar'), ('Fr', 'Fr'), ('Ar-Mg', 'Ar-Mg'), ('Mg-Fr', 'Mg-Fr'), ('Ar-Fr', 'Ar-Fr')], default='Mg', max_length=100)),
                ('quantite_entree', models.IntegerField(blank=True, default=0, null=True)),
                ('quantite_sortie', models.IntegerField(blank=True, default=0, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('centre', models.CharField(choices=[('Antaniavo', 'Antaniavo'), ('Andakana', 'Andakana'), ('Manakara', 'Manakara')], default='Antaniavo', max_length=100)),
                ('date_entree', models.DateField(blank=True, null=True)),
                ('date_sortie', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HistoriqueDepotLivre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('action', models.CharField(choices=[('entree', 'entree'), ('sortie', 'sortie')], max_length=100)),
                ('qantite', models.IntegerField(default=0)),
                ('motif', models.CharField(blank=True, max_length=1000, null=True)),
                ('nom', models.CharField(blank=True, max_length=100, null=True)),
                ('reference', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.depotlivre')),
            ],
        ),
    ]
