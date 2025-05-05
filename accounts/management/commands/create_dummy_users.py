# accounts/management/commands/create_dummy_users.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models   import User
from accounts.models              import Profile

class Command(BaseCommand):
    help = "Create dummy users for every role with password 'password123'"

    def handle(self, *args, **options):
        users = [
            ('alice',  'password123', 'student'),
            ('bob',    'password123', 'hall_clerk'),
            ('carol',  'password123', 'mess_manager'),
            ('david',  'password123', 'warden'),
            ('edward', 'password123', 'finance_officer'),
            ('faythe', 'password123', 'staff_admin'),
        ]

        for username, pw, role in users:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(pw)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user {username}"))
            else:
                self.stdout.write(f"User {username} already exists")

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()
            self.stdout.write(self.style.SUCCESS(f" → role set to {role}, password '{pw}'"))