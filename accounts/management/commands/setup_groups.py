from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Create groups with appropriate permissions for the marketplace'

    def handle(self, *args, **options):
        # --- Admin Group (Full Access) ---
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        all_perms = Permission.objects.all()
        admin_group.permissions.set(all_perms)
        self.stdout.write(self.style.SUCCESS('Admin group created with full permissions.'))

        # --- Seller Group ---
        seller_group, _ = Group.objects.get_or_create(name='Seller')
        seller_perms = Permission.objects.filter(
            content_type__app_label='Product',
            codename__in=[
                'view_product', 'add_product', 'change_product',
                'view_category',
            ],
        )
        seller_perms |= Permission.objects.filter(
            content_type__app_label='accounts',
            codename__in=['view_seller', 'change_seller'],
        )
        seller_perms |= Permission.objects.filter(
            content_type__app_label='core',
            codename__in=['view_ad', 'view_sidead', 'view_bannerad', 'view_cardad'],
        )
        seller_perms |= Permission.objects.filter(
            content_type__app_label='blog',
            codename__in=['view_blog'],
        )
        seller_group.permissions.set(seller_perms)
        self.stdout.write(self.style.SUCCESS('Seller group created with limited permissions.'))

        # --- Customer Group ---
        customer_group, _ = Group.objects.get_or_create(name='Customer')
        customer_perms = Permission.objects.filter(
            content_type__app_label='Product',
            codename__in=['view_product', 'view_category'],
        )
        customer_perms |= Permission.objects.filter(
            content_type__app_label='accounts',
            codename__in=['view_customer', 'change_customer'],
        )
        customer_perms |= Permission.objects.filter(
            content_type__app_label='core',
            codename__in=['view_ad', 'view_sidead', 'view_bannerad', 'view_cardad'],
        )
        customer_perms |= Permission.objects.filter(
            content_type__app_label='blog',
            codename__in=['view_blog'],
        )
        customer_group.permissions.set(customer_perms)
        self.stdout.write(self.style.SUCCESS('Customer group created with read-only permissions.'))
