from django.contrib.auth.decorators import user_passes_test

def role_required(*roles):
    """
    Only allow users whose Profile.role is in the given roles.
    """
    return user_passes_test(
        lambda u: (
            u.is_authenticated
            and hasattr(u, 'profile')
            and u.profile.role in roles
        ),
        login_url='login'
    )
