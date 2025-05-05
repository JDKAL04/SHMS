# core/migrations/0001_create_groups.py

from django.db import migrations

def create_groups(apps, schema_editor):
    Group      = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Map each role to the permissions they need (model codenames)
    role_perms = {
        'Clerk': [
            'add_student','change_student',
            'add_admission','change_admission',
            'view_payment','add_payment',
        ],
        'Mess Manager': [
            'add_messcharge','change_messcharge','view_messcharge'
        ],
        'Warden': [
            'view_complaint','add_actiontakenreport','change_actiontakenreport',
            'view_allocation','view_grantexpenditure'
        ],
        'Controlling Warden': [
            'view_allocation','add_grantexpenditure','view_grantexpenditure',
            'view_pettyexpense'
        ],
        'Staff': [
            'view_attendance','view_payroll'
        ],
        'Student': [
            'add_complaint','view_complaint','view_payment','view_dues_overview'
        ],
    }

    for role, codenames in role_perms.items():
        grp, _ = Group.objects.get_or_create(name=role)
        for codename in codenames:
            try:
                perm = Permission.objects.get(codename=codename)
                grp.permissions.add(perm)
            except Permission.DoesNotExist:
                # skipped if codename not found
                pass

class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]
    operations = [
        migrations.RunPython(create_groups, reverse_code=migrations.RunPython.noop),
    ]
