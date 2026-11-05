from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
    SiteSetting, HeroSlide, Program, Course, AdmissionBatch, 
    AdmissionCandidate, StaffMember, NewsEvent, FAQ, InquiryMessage
)
import datetime


class Command(BaseCommand):
    help = 'Seed authentic NSUK ODeL database records matching odel.nsuk.edu.ng'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding NSUK ODeL database..."))

        # 1. Admin Superuser
        admin_user, created = User.objects.get_or_create(username='admin')
        if created or not admin_user.check_password('admin@123'):
            admin_user.set_password('admin@123')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.first_name = "ODeL"
            admin_user.last_name = "Administrator"
            admin_user.email = "admin@odel.nsuk.edu.ng"
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user (admin / admin@123)"))

        # 2. Site Settings
        settings = SiteSetting.get_settings()
        settings.site_name = "Nasarawa State University, Keffi"
        settings.center_name = "Directorate of Open, Distance and e-Learning (ODeL)"
        settings.center_acronym = "NSUK ODeL"
        settings.top_announcement = "Our pioneer Programme is B.Sc Public Administration • 2025/2026 Admissions Open"
        settings.tagline = "Knowledge for Development - Flexible, High-Quality Degree Programs Anywhere"
        settings.contact_email = "support@odel.nsuk.edu.ng"
        settings.contact_phone_1 = "+234 902 350 0752"
        settings.contact_phone_2 = "+234 803 293 8812"
        settings.whatsapp_number = "2349023500752"
        settings.address = "Directorate of Open, Distance and e-Learning (ODeL), Nasarawa State University, PMB 1022, Keffi, Nasarawa State, Nigeria"
        settings.student_portal_url = "https://ug.nsuk.edu.ng/login/"
        settings.application_portal_url = "https://ug.nsuk.edu.ng/application/#/"
        settings.pgd_application_url = "https://pg.nsuk.edu.ng/application/#/"
        settings.lms_portal_url = "https://lms.nsuk.edu.ng/"
        settings.library_portal_url = "https://nsuk.edu.ng/library/"
        settings.vc_name = "Prof. Sa'adatu Hassan Liman, FELLOW: ASAS, FIPMA, FICA, FHEA(UK)"
        settings.vc_title = "Vice-Chancellor, Nasarawa State University, Keffi"
        settings.vc_image = "leadership/vc.jpg"
        settings.director_name = "Prof. Benneth Colman Uzoechi"
        settings.director_title = "Director, Directorate of Open, Distance and e-Learning"
        settings.director_image = "leadership/director.jpg"
        settings.save()

        # 3. Hero Slides
        HeroSlide.objects.all().delete()
        slides_data = [
            {
                'title': "Study B.Sc Public Administration Online",
                'subtitle': "Flexible, NUC-accredited Bachelor of Science program designed for working professionals and ambitious scholars.",
                'badge_text': "Pioneer Program",
                'image_url_fallback': "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1600&q=80",
                'cta_primary_text': "Apply Now",
                'cta_primary_url': "/admissions/how-to-apply/",
                'cta_secondary_text': "Check Admission List",
                'cta_secondary_url': "/admission-list/",
                'display_order': 1
            },
            {
                'title': "2025/2026 Provisional Admission List Released",
                'subtitle': "Check the official list of admitted candidates for the Open Distance & e-Learning undergraduate session.",
                'badge_text': "Admission Update",
                'image_url_fallback': "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1600&q=80",
                'cta_primary_text': "Verify Admission",
                'cta_primary_url': "/admission-list/",
                'cta_secondary_text': "Student Portal",
                'cta_secondary_url': "https://ug.nsuk.edu.ng/login/",
                'display_order': 2
            },
            {
                'title': "Modern CBT & Interactive Learning Management System",
                'subtitle': "Learn from your location at your pace with full digital classroom support, tutor interaction, and proctored CBT assessments.",
                'badge_text': "100% CBT Assessment",
                'image_url_fallback': "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1600&q=80",
                'cta_primary_text': "Access LMS",
                'cta_primary_url': "https://lms.nsuk.edu.ng/",
                'cta_secondary_text': "Browse Courses",
                'cta_secondary_url': "/courses/",
                'display_order': 3
            },
        ]
        for s in slides_data:
            HeroSlide.objects.create(**s)

        # 4. Academic Programs
        Program.objects.all().delete()
        prog_pub_admin = Program.objects.create(
            name="B.Sc Public Administration",
            slug="b-sc-public-administration",
            degree_type="B.Sc",
            faculty="Faculty of Administration",
            department="Department of Public Administration",
            status="Active",
            duration="2 - 4 Years (Flexible Semesters)",
            short_description="Our flagship pioneer program providing rigorous grounding in public management, administrative law, governance, policy analysis, and organizational leadership.",
            full_overview=(
                "The B.Sc Public Administration program at NSUK ODeL is structured to produce high-caliber administrators, "
                "policy analysts, and governance professionals. Delivered via our state-of-the-art Learning Management System, "
                "students engage with cutting-edge coursework in administrative theory, personnel management, development administration, "
                "public financial management, and comparative governance.\n\n"
                "The curriculum combines asynchronous self-paced digital study with live facilitator sessions, case studies, "
                "and objective Computer-Based Testing (CBT) examinations."
            ),
            utme_requirements="Five (5) O'Level credit passes in English Language, Mathematics, Government/History, Economics and any other Social Science/Arts subject at not more than two sittings.",
            direct_entry_requirements="National Diploma (ND) with minimum of Lower Credit, NCE with merit, or IJMB/GCE 'A' Level with passes in relevant subjects.",
            conversion_requirements="Higher National Diploma (HND) or a Bachelor's degree in any discipline for 300 Level Entry (Fast-track 2-Year Program).",
            career_opportunities="Federal, State and Local Civil Service, Public Policy Think Tanks, Non-Governmental Organizations (NGOs), International Development Agencies (UN, AU, ECOWAS), Human Resource Management, Corporate Affairs.",
            featured_image_url="https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80",
            is_featured=True,
            is_active=True,
            display_order=1
        )

        upcoming_programs = [
            {
                'name': "B.Sc Computer Science",
                'slug': "b-sc-computer-science",
                'faculty': "Faculty of Natural & Applied Sciences",
                'department': "Department of Computer Science",
                'status': "Upcoming",
                'duration': "2 - 4 Years",
                'short_description': "Comprehensive software engineering, data science, networking, and computing technology degree.",
                'full_overview': "Prepares graduates for high-demand technology careers in software engineering, cybersecurity, AI, and systems analysis.",
                'featured_image_url': "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80",
                'display_order': 2
            },
            {
                'name': "B.Sc Business Administration",
                'slug': "b-sc-business-administration",
                'faculty': "Faculty of Administration",
                'department': "Department of Business Administration",
                'status': "Upcoming",
                'duration': "2 - 4 Years",
                'short_description': "Strategic management, marketing, organizational behavior, and corporate finance.",
                'full_overview': "Equips aspiring business leaders and managers with modern executive skills.",
                'featured_image_url': "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80",
                'display_order': 3
            },
            {
                'name': "B.Sc Accounting",
                'slug': "b-sc-accounting",
                'faculty': "Faculty of Administration",
                'department': "Department of Accounting",
                'status': "Upcoming",
                'duration': "2 - 4 Years",
                'short_description': "Financial reporting, auditing, taxation, management accounting, and corporate governance.",
                'full_overview': "Professional training for chartered accountancy and financial management.",
                'featured_image_url': "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80",
                'display_order': 4
            },
            {
                'name': "B.Sc Economics",
                'slug': "b-sc-economics",
                'faculty': "Faculty of Social Sciences",
                'department': "Department of Economics",
                'status': "Upcoming",
                'duration': "2 - 4 Years",
                'short_description': "Microeconomics, macroeconomics, econometrics, monetary policy, and development finance.",
                'full_overview': "Analytical understanding of markets, economic policies, and global finance.",
                'featured_image_url': "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=800&q=80",
                'display_order': 5
            },
            {
                'name': "B.Sc Entrepreneurship",
                'slug': "b-sc-entrepreneurship",
                'faculty': "Faculty of Administration",
                'department': "Department of Entrepreneurship",
                'status': "Upcoming",
                'duration': "2 - 4 Years",
                'short_description': "Venture creation, innovation management, business scaling, and digital enterprise development.",
                'full_overview': "Empowering innovators and enterprise creators with practical business acumen.",
                'featured_image_url': "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=800&q=80",
                'display_order': 6
            },
        ]
        for up in upcoming_programs:
            Program.objects.create(**up)

        # 5. Courses Catalog (Mirroring authentic courses on odel.nsuk.edu.ng)
        Course.objects.all().delete()
        courses_data = [
            {
                'program': prog_pub_admin,
                'course_code': "PAD111",
                'title': "Introduction to Public Administration I",
                'level': "100",
                'semester': "1st",
                'credit_units': 3,
                'description': "Foundational concepts, nature, scope and evolution of public administration as an academic discipline and practice.",
                'thumbnail_url': "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=600&q=80",
                'lms_url': "https://lms.nsuk.edu.ng/course/index.php?categoryid=522",
                'display_order': 1
            },
            {
                'program': prog_pub_admin,
                'course_code': "ECO111",
                'title': "Principles of Economics I",
                'level': "100",
                'semester': "1st",
                'credit_units': 3,
                'description': "Introduction to microeconomics, consumer behavior, market structures, price determination, and allocation of resources.",
                'thumbnail_url': "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=600&q=80",
                'lms_url': "https://lms.nsuk.edu.ng/course/index.php?categoryid=522",
                'display_order': 2
            },
            {
                'program': prog_pub_admin,
                'course_code': "ACC111",
                'title': "Introduction to Accounting",
                'level': "100",
                'semester': "1st",
                'credit_units': 3,
                'description': "Basic accounting principles, double-entry bookkeeping, trial balance, ledgers, and financial statement preparation.",
                'thumbnail_url': "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=600&q=80",
                'lms_url': "https://lms.nsuk.edu.ng/course/index.php?categoryid=522",
                'display_order': 3
            },
            {
                'program': prog_pub_admin,
                'course_code': "PAD112",
                'title': "Introduction to Public Administration II",
                'level': "100",
                'semester': "2nd",
                'credit_units': 3,
                'description': "Administrative theories, classical, neoclassical and modern models of bureaucracy, Weberian perspectives.",
                'thumbnail_url': "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80",
                'lms_url': "https://lms.nsuk.edu.ng/course/index.php?categoryid=522",
                'display_order': 4
            },
            {
                'program': prog_pub_admin,
                'course_code': "PAD211",
                'title': "Administrative Law",
                'level': "200",
                'semester': "1st",
                'credit_units': 3,
                'description': "Constitutional framework, delegated legislation, judicial review of administrative actions, and natural justice.",
                'thumbnail_url': "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=600&q=80",
                'lms_url': "https://lms.nsuk.edu.ng/course/index.php?categoryid=522",
                'display_order': 5
            },
            {
                'program': prog_pub_admin,
                'course_code': "PAD221",
                'title': "Nigerian Government & Politics",
                'level': "200",
                'semester': "2nd",
                'credit_units': 3,
                'description': "Historical development of the Nigerian state, federalism, constitutional development, and contemporary governance challenges.",
                'thumbnail_url': "https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=600&q=80",
                'lms_url': "https://lms.nsuk.edu.ng/course/index.php?categoryid=522",
                'display_order': 6
            },
            {
                'program': prog_pub_admin,
                'course_code': "PAD311",
                'title': "Public Policy Analysis",
                'level': "300",
                'semester': "1st",
                'credit_units': 3,
                'description': "Policy formulation, implementation models, monitoring and evaluation techniques in government and development agencies.",
                'thumbnail_url': "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=600&q=80",
                'lms_url': "https://lms.nsuk.edu.ng/course/index.php?categoryid=522",
                'display_order': 7
            },
            {
                'program': prog_pub_admin,
                'course_code': "PAD321",
                'title': "Public Financial Management",
                'level': "300",
                'semester': "2nd",
                'credit_units': 3,
                'description': "Government budgeting, fiscal federalism, treasury single account (TSA), and public sector audit standards.",
                'thumbnail_url': "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=600&q=80",
                'lms_url': "https://lms.nsuk.edu.ng/course/index.php?categoryid=522",
                'display_order': 8
            },
        ]
        for c in courses_data:
            Course.objects.create(**c)

        # 6. Admission Batches & Authentic Candidates from odel.nsuk.edu.ng
        AdmissionBatch.objects.all().delete()
        AdmissionCandidate.objects.all().delete()
        
        batch_1 = AdmissionBatch.objects.create(
            title="Provisional Admission First List",
            academic_session="2025/2026",
            is_active=True,
            description="Official first batch of candidates admitted into the NSUK ODeL Bachelor of Science in Public Administration program."
        )

        real_candidates_data = [
            (1, "LUKMAN Muhammed Sani", "ODEL2500008", "B.Sc Public Administration (ODEL)", "100", "Male", "Nasarawa"),
            (2, "OBIDUBA Chinonso Vincent", "ODEL2500128", "B.Sc Public Administration (ODEL)", "100", "Male", "Imo"),
            (3, "FABEKE Douglas Deeka", "ODEL2500039", "B.Sc Public Administration (ODEL)", "200", "Male", "Rivers"),
            (4, "IKPE Bright Dooshima", "ODEL2500209", "B.Sc Public Administration (ODEL)", "100", "Female", "Cross River"),
            (5, "ALAO Felix Omokaru", "ODEL2500058", "B.Sc Public Administration (ODEL)", "200", "Male", "Edo"),
            (6, "ONABE Promise Ushia", "ODEL2500067", "B.Sc Public Administration (ODEL)", "100", "Female", "Cross River"),
            (7, "IYIOLA Kabirat Otindamola Dami", "ODEL2500123", "B.Sc Public Administration (ODEL)", "200", "Female", "Oyo"),
            (8, "EGBINOLA Nafisat Tolani", "ODEL2500063", "B.Sc Public Administration (ODEL)", "100", "Female", "Oyo"),
            (9, "AGYE Enoch Ayeni", "ODEL2500098", "B.Sc Public Administration (ODEL)", "100", "Male", "Benue"),
            (10, "Nwaigwe Raymond Chidiebere", "ODEL2500133", "B.Sc Public Administration (ODEL)", "100", "Female", "Abia"),
            (11, "AHMED Samaila Goni", "ODEL2500096", "B.Sc Public Administration (ODEL)", "100", "Male", "Borno"),
            (12, "BELLO-BALOGUN Aisha Olufunmilola", "ODEL2500199", "B.Sc Public Administration (ODEL)", "100", "Female", "Oyo"),
            (13, "DAMLA Victoria Banahel", "ODEL2500127", "B.Sc Public Administration (ODEL)", "100", "Female", "Plateau"),
            (14, "SUNDAY Richard Ndukwe", "ODEL2500200", "B.Sc Public Administration (ODEL)", "100", "Male", "Abia"),
            (15, "BADAMASI Hassan", "ODEL2500146", "B.Sc Public Administration (ODEL)", "100", "Male", "Katsina"),
            (16, "AHMAD Abubakar Bage", "ODEL2500177", "B.Sc Public Administration (ODEL)", "100", "Male", "Nasarawa"),
            (17, "HUSSEIN Hanifat Onozasi", "ODEL2500165", "B.Sc Public Administration (ODEL)", "100", "Female", "Kogi"),
            (18, "OFREMU Anthonia Chinyere", "ODEL2500148", "B.Sc Public Administration (ODEL)", "100", "Female", "Delta"),
            (19, "SUDI Usman", "ODEL2500154", "B.Sc Public Administration (ODEL)", "200", "Male", "Adamawa"),
            (20, "USMAN Auwal", "ODEL2500159", "B.Sc Public Administration (ODEL)", "200", "Male", "Taraba"),
            (21, "SHUAIBU Aishatu Tukura", "ODEL2500163", "B.Sc Public Administration (ODEL)", "200", "Female", "Nasarawa"),
            (22, "BUHARI Bello Ali", "ODEL2500170", "B.Sc Public Administration (ODEL)", "200", "Male", "Kebbi"),
            (23, "TUKURAH Deborah", "ODEL2500195", "B.Sc Public Administration (ODEL)", "200", "Female", "Nasarawa"),
            (24, "SIMON Godiya Sinamai", "ODEL2500212", "B.Sc Public Administration (ODEL)", "200", "Female", "Adamawa"),
            (25, "TIEMO Banro Roland", "ODEL2500041", "B.Sc Public Administration (ODEL)", "200", "Male", "Delta"),
            (26, "DAMFUR Nelson Emmanuel", "ODEL2500121", "B.Sc Public Administration (ODEL)", "200", "Male", "Plateau"),
            (27, "GARBA Amina Mohammed", "ODEL2500215", "B.Sc Public Administration (ODEL)", "100", "Female", "Kaduna"),
            (28, "OKOYE Chibuike Stanley", "ODEL2500219", "B.Sc Public Administration (ODEL)", "200", "Male", "Anambra"),
            (29, "MOHAMMED Haruna Jibril", "ODEL2500224", "B.Sc Public Administration (ODEL)", "300", "Male", "Niger"),
            (30, "ADEBAYO Temitope Grace", "ODEL2500230", "B.Sc Public Administration (ODEL)", "300", "Female", "Lagos"),
        ]

        for sn, name, app_id, prog, lvl, sex, state in real_candidates_data:
            AdmissionCandidate.objects.create(
                batch=batch_1,
                serial_number=sn,
                candidate_name=name,
                applicant_id=app_id,
                program=prog,
                level_of_entry=lvl,
                gender=sex,
                state_of_origin=state,
                status="Admitted"
            )

        # 7. Authentic Staff & Facilitators Directory from odel.nsuk.edu.ng/our-staff/
        StaffMember.objects.all().delete()
        staff_data = [
            {
                'full_name': "Prof. Benneth Colman Uzoechi",
                'position': "Director",
                'category': "Leadership",
                'department': "Directorate of Open, Distance & e-Learning (ODeL)",
                'qualifications': "Ph.D, FIM, Professor",
                'biography': "Director of the Directorate of Open Distance and e-Learning (ODeL), Nasarawa State University, Keffi.",
                'photo': "staff/prof_benneth_uzoechi.jpg",
                'photo_url': "https://odel.nsuk.edu.ng/wp-content/uploads/2024/02/ODEL-DIRECTOR.jpg",
                'email': "director.odel@nsuk.edu.ng",
                'phone': "+234 902 350 0752",
                'sort_order': 1,
                'is_active': True,
            },
            {
                'full_name': "Dr. Salihu Abdullahi Audu",
                'position': "Deputy Director",
                'category': "Leadership",
                'department': "Directorate of Open, Distance & e-Learning (ODeL)",
                'qualifications': "Ph.D",
                'biography': "Deputy Director of the Directorate of Open Distance and e-Learning (ODeL), Nasarawa State University, Keffi.",
                'photo': "staff/dr_salihu_audu.jpg",
                'photo_url': "https://odel.nsuk.edu.ng/wp-content/uploads/2026/06/IMG_4099-1.jpg",
                'email': "deputy.director.odel@nsuk.edu.ng",
                'phone': "+234 902 350 0752",
                'sort_order': 2,
                'is_active': True,
            },
            {
                'full_name': "Dr. Odonye Dauda Yusuf",
                'position': "Programme Coordinator",
                'category': "Academic",
                'department": "Department of Public Administration / ODeL",
                'qualifications': "Ph.D",
                'biography': "Programme Coordinator for Open Distance and e-Learning programmes at NSUK.",
                'photo': "staff/dr_odonye_yusuf.jpg",
                'photo_url': "https://odel.nsuk.edu.ng/wp-content/uploads/2025/03/odonye.jpg",
                'email': "coordinator.odel@nsuk.edu.ng",
                'phone': "+234 902 350 0752",
                'sort_order': 3,
                'is_active': True,
            },
            {
                'full_name': "Dr. Iya Haruna Ayuba",
                'position': "Head, Guidance and Counselling",
                'category': "Academic",
                'department': "Guidance & Counselling Unit, ODeL",
                'qualifications': "Ph.D",
                'biography': "Head of Guidance and Counselling, supporting distance learning students with academic guidance and mentoring.",
                'photo': "staff/dr_iya_ayuba.jpg",
                'photo_url': "https://odel.nsuk.edu.ng/wp-content/uploads/2025/03/iyah.jpg",
                'email': "counselling.odel@nsuk.edu.ng",
                'phone': "+234 902 350 0752",
                'sort_order': 4,
                'is_active': True,
            },
            {
                'full_name': "Mrs. Hajara J Garba",
                'position': "ICT Coordinator",
                'category': "Technical",
                'department': "ODeL Information & Communication Technology Unit",
                'qualifications': "M.Sc, B.Sc",
                'biography': "ICT Coordinator managing technological infrastructure, digital classrooms, and network systems for ODeL.",
                'photo': "staff/mrs_hajara_garba.jpg",
                'photo_url': "https://odel.nsuk.edu.ng/wp-content/uploads/2025/03/HAJO.jpg",
                'email': "ict.odel@nsuk.edu.ng",
                'phone': "+234 902 350 0752",
                'sort_order': 5,
                'is_active': True,
            },
            {
                'full_name': "Dama Williams Yohanna",
                'position': "ODeL Webmaster/DB Analyst",
                'category': "Technical",
                'department': "ODeL Systems & Database Unit",
                'qualifications': "B.Sc, Webmaster & Database Administrator",
                'biography': "ODeL Webmaster and Database Analyst in charge of digital portals, LMS, database security, and web applications.",
                'photo': "staff/dama_williams_yohanna.jpg",
                'photo_url': "https://odel.nsuk.edu.ng/wp-content/uploads/2026/06/WhatsApp-Image-2026-06-08-at-10.02.13-AM.jpeg",
                'email': "webmaster.odel@nsuk.edu.ng",
                'phone': "+234 902 350 0752",
                'sort_order': 6,
                'is_active': True,
            },
            {
                'full_name': "Mr. Ibrahim Liman",
                'position': "ODeL Help Desk Officer",
                'category': "Technical",
                'department': "ODeL Learner Support & Help Desk Unit",
                'qualifications': "Support Specialist",
                'biography': "Help Desk Officer providing frontline student support, technical assistance, and LMS navigation guidance.",
                'photo': "staff/mr_ibrahim_liman.jpg",
                'photo_url': "https://odel.nsuk.edu.ng/wp-content/uploads/2025/03/ibro.jpeg",
                'email': "helpdesk.odel@nsuk.edu.ng",
                'phone': "+234 902 350 0752",
                'sort_order': 7,
                'is_active': True,
            },
            {
                'full_name': "Mrs. Zainab Maikasuwa",
                'position': "ODeL Secretary",
                'category': "Administrative",
                'department': "ODeL Directorate Secretariat",
                'qualifications': "Secretarial Administration",
                'biography': "Directorate Secretary managing administrative documentation, confidential correspondence, and executive coordination.",
                'photo': "staff/mrs_zainab_maikasuwa.jpg",
                'photo_url': "https://odel.nsuk.edu.ng/wp-content/uploads/2025/03/WhatsApp-Image-2025-03-05-at-3.12.03-AM.jpeg",
                'email': "secretary.odel@nsuk.edu.ng",
                'phone': "+234 902 350 0752",
                'sort_order': 8,
                'is_active': True,
            },
            {
                'full_name': "Dr. Yakubu Jacob Umaru",
                'position': "Programmes & Editorial Coordinator",
                'category': "Academic",
                'department': "ODeL Academic & Editorial Unit",
                'qualifications': "Ph.D",
                'biography': "Programmes and Editorial Coordinator supervising instructional courseware design, module peer review, and editorial quality.",
                'photo': "staff/dr_yakubu_umaru.jpg",
                'photo_url': "https://odel.nsuk.edu.ng/wp-content/uploads/2025/04/WhatsApp-Image-2025-04-15-at-4.59.41-AM.jpeg",
                'email': "editorial.odel@nsuk.edu.ng",
                'phone': "+234 902 350 0752",
                'sort_order': 9,
                'is_active': True,
            },
            {
                'full_name': "Mr. Kumiyawo James Ayinda",
                'position': "Finance Officer",
                'category': "Administrative",
                'department': "ODeL Finance & Accounts Unit",
                'qualifications': "B.Sc, Accountant",
                'biography': "Finance Officer managing student fee administration, accounting reconciliations, and budget compliance.",
                'photo': "staff/mr_kumiyawo_ayinda.jpg",
                'photo_url': "https://odel.nsuk.edu.ng/wp-content/uploads/2025/04/WhatsApp-Image-2025-04-14-at-3.44.57-AM-1.jpeg",
                'email': "finance.odel@nsuk.edu.ng",
                'phone': "+234 902 350 0752",
                'sort_order': 10,
                'is_active': True,
            },
            {
                'full_name': "Dr. Ossai Onyeka Peter",
                'position': "E-Tutor",
                'category': "Academic",
                'department': "ODeL Academic Facilitation Unit",
                'qualifications': "Ph.D",
                'biography': "E-Tutor conducting online seminars, virtual study sessions, continuous assessments, and academic tutoring.",
                'photo': "staff/dr_ossai_peter.jpg",
                'photo_url': "https://odel.nsuk.edu.ng/wp-content/uploads/2025/11/osai.jpeg",
                'email': "tutor.ossai@nsuk.edu.ng",
                'phone': "+234 902 350 0752",
                'sort_order': 11,
                'is_active': True,
            },
            {
                'full_name': "Mr. Sini Obidah",
                'position': "E-Tutor",
                'category': "Academic",
                'department': "ODeL Academic Facilitation Unit",
                'qualifications': "M.Sc, Facilitator",
                'biography': "E-Tutor facilitating distance learning lectures, course forum discussions, and online student academic tutoring.",
                'photo': "staff/mr_sini_obidah.jpg",
                'photo_url': "https://odel.nsuk.edu.ng/wp-content/uploads/2025/04/WhatsApp-Image-2025-04-03-at-4.26.40-AM.jpeg",
                'email': "tutor.sini@nsuk.edu.ng",
                'phone': "+234 902 350 0752",
                'sort_order': 12,
                'is_active': True,
            },
        ]
        for s in staff_data:
            StaffMember.objects.create(**s)

        # 8. News & Events
        NewsEvent.objects.all().delete()
        news_data = [
            {
                'title': "NUC Approves Commencement of Open Distance e-Learning For NSUK, Program To Kick-off With B.Sc Public Administration",
                'slug': "nuc-approves-commencement-of-open-distance-e-learning-for-nsuk-program-to-kick-off-with-b-sc-public-administration",
                'category': "Events",
                'excerpt': "In its bid to further the frontiers of education and make it more accessible to the generality of the public, the National Universities Commission (NUC) has given formal approval to NSUK.",
                'content': (
                    "The National Universities Commission (NUC) has officially granted approval to Nasarawa State University, Keffi (NSUK) "
                    "to commence academic activities in its Directorate of Open, Distance, and e-Learning (ODeL).\n\n"
                    "The center will pioneer with the accredited Bachelor of Science (B.Sc) in Public Administration. The Vice-Chancellor "
                    "commended the Directorate for meeting all stringent regulatory quality standards in instructional materials, "
                    "LMS readiness, and robust CBT testing environments."
                ),
                'featured_image_url': "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=800&q=80",
                'is_featured': True,
                'is_active': True
            },
            {
                'title': "Application Portal Open for 2025/2026 Academic Session",
                'slug': "application-open-2025-2026",
                'category': "Application",
                'excerpt': "Applications are officially invited from suitably qualified candidates for admission into the B.Sc Public Administration ODeL degree program.",
                'content': (
                    "Prospective students can now apply online via the NSUK undergraduate application portal. "
                    "The program accommodates 100 Level (UTME), 200 Level (Direct Entry), and 300 Level (HND/Degree conversion candidates). "
                    "Applications will be processed on a rolling admission schedule."
                ),
                'featured_image_url': "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80",
                'is_featured': True,
                'is_active': True
            },
            {
                'title': "Orientation and LMS Training Session for Newly Admitted Students",
                'slug': "orientation-and-lms-training-session",
                'category': "Academic",
                'excerpt': "Virtual orientation and technical walkthrough on accessing digital modules, submitting assignments, and taking CBT quizzes.",
                'content': (
                    "All newly admitted students in the first admission list are invited to attend the comprehensive virtual orientation. "
                    "The session will cover navigation of the Moodle LMS, participating in facilitator discussion forums, and troubleshooting access."
                ),
                'featured_image_url': "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=800&q=80",
                'is_featured': False,
                'is_active': True
            }
        ]
        for n in news_data:
            NewsEvent.objects.create(**n)

        # 9. FAQs (Matching odel.nsuk.edu.ng FAQ list exactly)
        FAQ.objects.all().delete()
        faqs_data = [
            {
                'question': "How do I apply for the ODeL programs?",
                'answer': "Click on 'Apply Now' on the portal, create your account, generate your Remita RRR payment invoice, and fill out the online application form with your academic credentials.",
                'category': "Admissions",
                'sort_order': 1
            },
            {
                'question': "What is the duration of the programme?",
                'answer': "Four (4) years for UTME candidates (8 semesters); Three (3) years for DIRECT ENTRY candidates (6 semesters); and Two (2) years for 300 Level Conversion candidates with HND/B.Sc qualifications (4 semesters).",
                'category': "Academic",
                'sort_order': 2
            },
            {
                'question': "Which course can I apply for currently?",
                'answer': "Our pioneer program is B.Sc in Public Administration. Proposed approved upcoming programs include B.Sc Computer Science, B.Sc Business Administration, B.Sc Accounting, B.Sc Entrepreneurship, and B.Sc Economics.",
                'category': "Admissions",
                'sort_order': 3
            },
            {
                'question': "Does the program have an age limit?",
                'answer': "No. There is no age limit. The distance learning model is designed for lifelong learners, working professionals, and mature applicants of all ages.",
                'category': "General",
                'sort_order': 4
            },
            {
                'question': "Do I have to be physically present at the University in Keffi?",
                'answer': "No. You can learn from your home or workplace anywhere in Nigeria or abroad. All lectures, study modules, and tutor discussions take place online.",
                'category': "LMS",
                'sort_order': 5
            },
            {
                'question': "How are examinations conducted?",
                'answer': "All our semester examinations are purely Computer-Based Testing (CBT), held in proctored digital centers.",
                'category': "LMS",
                'sort_order': 6
            },
            {
                'question': "Is the NSUK ODeL degree certificate the same as regular on-campus degrees?",
                'answer': "Yes. The certificate awarded upon graduation is the official, NUC-accredited Bachelor of Science (B.Sc) from Nasarawa State University, Keffi, with equal standing for civil service, corporate employment, and postgraduate studies worldwide.",
                'category': "General",
                'sort_order': 7
            }
        ]
        for f in faqs_data:
            FAQ.objects.create(**f)

        self.stdout.write(self.style.SUCCESS("Successfully seeded NSUK ODeL complete database!"))
