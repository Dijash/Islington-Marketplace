from django.db import migrations, models
import django.db.models.deletion


def migrate_product_categories_to_model(apps, schema_editor):
    Product = apps.get_model('Product', 'Product')
    Category = apps.get_model('Product', 'Category')

    category_names = (
        Product.objects.exclude(category='')
        .exclude(category__isnull=True)
        .values_list('category', flat=True)
        .distinct()
    )

    for raw_name in category_names:
        name = raw_name.strip()
        if not name:
            continue
        Category.objects.get_or_create(name=name)

    for product in Product.objects.all():
        raw_name = (product.category or '').strip()
        if not raw_name:
            continue
        category = Category.objects.filter(name=raw_name).first()
        if category:
            product.category_ref = category
            product.save(update_fields=['category_ref'])


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0002_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category_ref',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='Product.category'),
        ),
        migrations.RunPython(migrate_product_categories_to_model, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='category_ref',
            new_name='category',
        ),
    ]
