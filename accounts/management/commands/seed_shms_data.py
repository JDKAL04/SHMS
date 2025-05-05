# accounts/management/commands/seed_shms_users_and_students.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models   import User
from accounts.models              import Profile
from students.models             import Student, Admission
from halls.models                import Hall, Room

class Command(BaseCommand):
    help = "Seed SHMS with users, profiles, one student, and its admission (assuming halls & rooms exist with exact names)."

    def handle(self, *args, **options):
        # 1) Create Users + Profiles
        users = [
            ('alice',  'password123', 'student'),
            ('bob',    'password123', 'hall_clerk'),
            ('carol',  'password123', 'mess_manager'),
            ('david',  'password123', 'warden'),
            ('edward', 'password123', 'finance_officer'),
            ('faythe', 'password123', 'staff_admin'),
        ]
        for uname, pw, role in users:
            user, created = User.objects.get_or_create(username=uname)
            if created:
                user.set_password(pw)
                user.is_staff = (role != 'student')
                user.save()
            Profile.objects.update_or_create(user=user, defaults={'role':role})
            self.stdout.write(self.style.SUCCESS(f"User: {uname} → {role}"))

        # 2) Create Student record for alice
        try:
            alice = User.objects.get(username='alice')
            student, _ = Student.objects.update_or_create(
                user=alice,
                defaults={
                    'name': 'Alice Johnson',
                    'address': '42 Maple Avenue, Springfield',
                    'phone': '9876543210',
                    'photo': '',
                }
            )
            self.stdout.write(self.style.SUCCESS("Student record for alice created"))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("alice user not found"))
            return

        # Hall names exactly as in DB:
        new_hall_name = 'Silver Oak Hall (New)'
        old_hall_name = 'Pine Crest Hall (old)'

        # 3) Create Admission for alice
        try:
            hall = Hall.objects.get(name=new_hall_name)
            room = Room.objects.get(hall=hall, number='101')
            Admission.objects.update_or_create(
                student=student,
                defaults={'hall':hall, 'room':room}
            )
            self.stdout.write(self.style.SUCCESS(
                f"Admission for alice → {new_hall_name} Room 101"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to create admission: {e}"))
            return

        self.stdout.write(self.style.SUCCESS("SHMS users & student seeding complete."))