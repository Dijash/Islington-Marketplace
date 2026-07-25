from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_blog'),
    ]

    operations = [
        migrations.RunSQL(
            sql='',
            reverse_sql='',
            hints={'table_name': 'core_blog'},
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='Blog',
                ),
            ],
            database_operations=[],
        ),
        migrations.AlterModelOptions(
            name='ad',
            options={'ordering': ['order', '-created_at'], 'verbose_name': 'Hero Ad', 'verbose_name_plural': 'Hero Ads'},
        ),
        migrations.AlterModelOptions(
            name='bannerad',
            options={'ordering': ['order', '-created_at'], 'verbose_name': 'Banner Ad', 'verbose_name_plural': 'Banner Ads'},
        ),
        migrations.AlterModelOptions(
            name='cardad',
            options={'ordering': ['order', '-created_at'], 'verbose_name': 'Card Ad', 'verbose_name_plural': 'Card Ads'},
        ),
        migrations.AlterModelOptions(
            name='sidead',
            options={'ordering': ['order', '-created_at'], 'verbose_name': 'Side Ad', 'verbose_name_plural': 'Side Ads'},
        ),
    ]
