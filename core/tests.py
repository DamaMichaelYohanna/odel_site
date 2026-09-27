from django.test import TestCase, Client
from django.urls import reverse
from core.models import SiteSetting, Program, Course, AdmissionBatch, AdmissionCandidate, InquiryMessage, FAQ, NewsEvent

class PublicPortalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.setting = SiteSetting.get_settings()
        self.program = Program.objects.create(
            name="B.Sc Public Administration",
            slug="b-sc-public-administration",
            status="Active"
        )
        self.course = Course.objects.create(
            program=self.program,
            course_code="PAD111",
            title="Introduction to Public Administration I",
            level="100",
            semester="1st",
            credit_units=3
        )
        self.batch = AdmissionBatch.objects.create(
            title="Provisional Admission First List",
            academic_session="2025/2026",
            is_active=True
        )
        self.candidate = AdmissionCandidate.objects.create(
            batch=self.batch,
            serial_number=1,
            candidate_name="LUKMAN Muhammed Sani",
            applicant_id="ODEL2500008",
            program="B.Sc Public Administration (ODEL)",
            level_of_entry="100",
            gender="Male",
            state_of_origin="Nasarawa",
            status="Admitted"
        )
        self.faq = FAQ.objects.create(
            question="How do I apply?",
            answer="Click apply now on the portal.",
            category="Admissions"
        )
        self.news = NewsEvent.objects.create(
            title="NUC Approves ODeL",
            slug="nuc-approves-odel",
            category="Events",
            excerpt="NUC has approved NSUK ODeL.",
            content="Full content here."
        )

    def test_homepage_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "NSUK")
        self.assertContains(response, "PAD111")

    def test_history_page(self):
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nasarawa State University, Keffi was established in 2001")

    def test_vc_message_page(self):
        response = self.client.get(reverse('vc_message'))
        self.assertEqual(response.status_code, 200)

    def test_director_message_page(self):
        response = self.client.get(reverse('director_message'))
        self.assertEqual(response.status_code, 200)

    def test_programs_and_detail(self):
        response = self.client.get(reverse('programs_list'))
        self.assertEqual(response.status_code, 200)
        
        detail_res = self.client.get(reverse('program_detail', kwargs={'slug': 'b-sc-public-administration'}))
        self.assertEqual(detail_res.status_code, 200)
        self.assertContains(detail_res, "B.Sc Public Administration")

    def test_courses_catalog(self):
        response = self.client.get(reverse('courses_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PAD111")

    def test_admission_list_view(self):
        response = self.client.get(reverse('admission_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ODEL2500008")
        self.assertContains(response, "LUKMAN Muhammed Sani")

    def test_admission_api_verification(self):
        # Found
        response = self.client.get(reverse('check_admission_api'), {'applicant_id': 'ODEL2500008'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['found'])
        self.assertEqual(data['candidate']['name'], "LUKMAN Muhammed Sani")
        
        # Not found
        res_not_found = self.client.get(reverse('check_admission_api'), {'applicant_id': 'INVALID999'})
        self.assertFalse(res_not_found.json()['found'])

    def test_contact_form_submission(self):
        response = self.client.post(reverse('contact'), {
            'full_name': 'Test Student',
            'email': 'student@example.com',
            'phone': '08012345678',
            'program_of_interest': 'B.Sc Public Administration',
            'subject': 'Admission Question',
            'message': 'When does the semester start?'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(InquiryMessage.objects.filter(email='student@example.com').exists())

    def test_faq_and_news(self):
        faq_res = self.client.get(reverse('faq'))
        self.assertEqual(faq_res.status_code, 200)
        self.assertContains(faq_res, "How do I apply?")
        
        news_res = self.client.get(reverse('news_list'))
        self.assertEqual(news_res.status_code, 200)
        
        detail_res = self.client.get(reverse('news_detail', kwargs={'slug': 'nuc-approves-odel'}))
        self.assertEqual(detail_res.status_code, 200)
