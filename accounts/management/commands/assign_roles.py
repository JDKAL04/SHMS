from django.core.management.base import BaseCommand
from django.contrib.auth.models   import User
from accounts.models              import Profile

class Command(BaseCommand):
    help = "Assign roles to existing users in bulk"

    def handle(self, *args, **options):
        mapping = {
            'alice':  'student',
            'bob':    'hall_clerk',
            'carol':  'mess_manager',
            'david':  'warden',
            'edward': 'finance_officer',
            'faythe': 'staff_admin',
        }

        for username, role in mapping.items():
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"No such user: {username}"))
                continue

            Profile.objects.update_or_create(
                user=user,
                defaults={'role': role}
            )
            self.stdout.write(self.style.SUCCESS(f"{username} → {role}"))

        self.stdout.write(self.style.SUCCESS("Done assigning roles."))