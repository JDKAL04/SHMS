# shms/shms/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import role_dashboard

urlpatterns = [
    # 1. Admin site
    path('admin/', admin.site.urls),

    # 2. Login/Logout pages
   path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout'
    ),

    path('accounts/', include('django.contrib.auth.urls')),
    # 3. Landing page: sends each user to their role dashboard
    path('', role_dashboard, name='home'),

    # 4. Your apps
    path('students/',   include(('students.urls',   'students'),   namespace='students')),
    path('mess/',       include(('mess.urls',       'mess'),       namespace='mess')),
    path('finances/',   include(('finances.urls',   'finances'),   namespace='finances')),
    path('complaints/', include(('complaints.urls', 'complaints'), namespace='complaints')),
    path('staff/',      include(('staff.urls',      'staff'),      namespace='staff')),
    path('halls/',      include(('halls.urls',      'halls'),      namespace='halls')),
    path('payments/',   include(('payments.urls',   'payments'),   namespace='payments')),
]