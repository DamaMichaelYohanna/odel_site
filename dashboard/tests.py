import io
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from core.models import AdmissionBatch, AdmissionCandidate, Program, Course, NewsEvent, FAQ

class DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='password123'
        )
        self.batch = AdmissionBatch.objects.create(
            title="First Batch Test",
            academic_session="2025/2026",
            is_active=True
        )

    def test_unauthenticated_redirect(self):
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/dashboard/login/' in response.url)

    def test_authenticated_dashboard_access(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ODeL Overview")

    def test_create_candidate_via_dashboard(self):
        self.client.login(username='admin_test', password='password123')
        post_data = {
            'batch': self.batch.id,
            'serial_number': 1,
            'candidate_name': 'Jane Doe',
            'applicant_id': 'ODEL2500999',
            'program': 'B.Sc Public Administration (ODEL)',
            'level_of_entry': '100',
            'gender': 'Female',
            'state_of_origin': 'Nasarawa',
            'status': 'Admitted'
        }
        response = self.client.post(reverse('dashboard_candidate_create'), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(AdmissionCandidate.objects.filter(applicant_id='ODEL2500999').exists())

    def test_bulk_csv_upload(self):
        self.client.login(username='admin_test', password='password123')
        csv_content = (
            "S/N,NAME,APPLICANT ID,PROGRAM,LEVEL OF ENTRY,SEX,STATE\n"
            "1,Aliyu Danladi,ODEL2500888,B.Sc Public Administration (ODEL),200,Male,Kano\n"
            "2,Fatima Yusuf,ODEL2500889,B.Sc Public Administration (ODEL),100,Female,Kaduna\n"
        )
        csv_file = SimpleUploadedFile("test_admission.csv", csv_content.encode('utf-8'), content_type="text/csv")
        
        response = self.client.post(reverse('dashboard_bulk_upload'), {
            'batch': self.batch.id,
            'csv_file': csv_file,
            'overwrite_existing': True
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(AdmissionCandidate.objects.filter(applicant_id='ODEL2500888').exists())
        self.assertTrue(AdmissionCandidate.objects.filter(applicant_id='ODEL2500889').exists())

    def test_sample_csv_download(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.get(reverse('dashboard_sample_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertContains(response, "ODEL2500008")
