from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from core.models import Role
from core.roles import ROLE_PERMISSIONS

class Command(BaseCommand):
    help = 'Assigns permissions to roles dynamically'

    def handle(self, *args, **options):
        for role_name, perm_codenames in ROLE_PERMISSIONS.items():
            role, created = Role.objects.get_or_create(name=role_name)
            print(f"{'Created' if created else 'Using'} role: {role_name}")

            for codename in perm_codenames:
                found = False
                for model in apps.get_models():
                    content_type = ContentType.objects.get_for_model(model)
                    try:
                        permission = Permission.objects.get(codename=codename, content_type=content_type)
                        role.permissions.add(permission)
                        found = True
                        print(f"  ✓ Assigned permission '{codename}' from model {model.__name__}")
                        break
                    except Permission.DoesNotExist:
                        continue

                if not found:
                    print(f"  ✗ Permission not found: {codename}")

            print(f"Finished assigning permissions for role: {role_name}\n")
