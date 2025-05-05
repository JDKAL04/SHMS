# shms/accounts/views.py

from django.shortcuts                   import redirect
from django.contrib.auth.decorators    import login_required

@login_required
def role_dashboard(request):
    """
    Send each user to the right landing page based on Profile.role.
    """
    role = request.user.profile.role

    if role == 'student':
        # that path now exists → /students/my-admissions/
        return redirect('students:my_admissions')

    elif role == 'hall_clerk':
        return redirect('students:admission_list')

    elif role == 'mess_manager':
        return redirect('mess:messcharge_list')

    elif role == 'warden':
        return redirect('halls:overall_occupancy')

    elif role == 'finance_officer':
        return redirect('finances:allocation_report')

    elif role == 'staff_admin':
        return redirect('staff:attendance_list')

    # fallback to login if role is missing or unrecognized
    return redirect('login')