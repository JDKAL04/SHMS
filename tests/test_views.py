# app1/tests/test_views.py
from django.urls import reverse
from django.test import TestCase

class StudentListViewTest(TestCase):
    def test_redirect_if_not_logged_in(self):
        url = reverse('app1:student_list')
        response = self.client.get(url)
        # Assuming login_required on this view
        self.assertRedirects(response, '/accounts/login/?next=' + url)

    def test_view_uses_correct_template(self):
        self.client.force_login(self._create_staff_user())
        response = self.client.get(reverse('app1:student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app1/student_list.html')
