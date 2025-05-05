# assign_roles.py
from django.contrib.auth.models import User
from accounts.models              import Profile

# Map usernames → roles
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
        print(f"⚠️  No such user: {username}")
        continue

    Profile.objects.update_or_create(
        user=user,
        defaults={'role': role}
    )
    print(f"✅  {username} → role set to {role}")

print("All done!")