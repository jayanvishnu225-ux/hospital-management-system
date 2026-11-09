from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_doctors'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='doctors',
            new_name='Doctor',
        ),
    ]
