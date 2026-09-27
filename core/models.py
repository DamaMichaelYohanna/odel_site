import os
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class SiteSetting(models.Model):
    """Global configuration and dynamic settings for the NSUK ODeL portal."""
    site_name = models.CharField(max_length=255, default="Nasarawa State University, Keffi")
    center_name = models.CharField(max_length=255, default="Directorate of Open, Distance and e-Learning (ODeL)")
    center_acronym = models.CharField(max_length=50, default="NSUK ODeL")
    top_announcement = models.CharField(max_length=300, default="Our pioneer Programme is B.Sc Public Administration • 2025/2026 Admission is currently ongoing!")
    tagline = models.CharField(max_length=300, default="Knowledge for Development - Flexible, Accessible & Quality Higher Education Anywhere")
    
    # Official contact & support
    contact_email = models.EmailField(default="support@odel.nsuk.edu.ng")
    contact_phone_1 = models.CharField(max_length=50, default="+234 902 350 0752")
    contact_phone_2 = models.CharField(max_length=50, blank=True, default="+234 803 000 0000")
    whatsapp_number = models.CharField(max_length=50, default="2349023500752", help_text="Digits only without +, e.g. 2349023500752")
    address = models.TextField(default="Directorate of Open, Distance and e-Learning (ODeL), Nasarawa State University, PMB 1022, Keffi, Nasarawa State, Nigeria")
    
    # Social links
    facebook_url = models.URLField(blank=True, default="https://www.facebook.com/share/GeQbjRVnquDncZzX/?mibextid=qi2Omg")
    twitter_x_url = models.URLField(blank=True, default="https://x.com/NSUKODeL?t=2rXQmautmJQRQGskHr91FQ&s=09")
    instagram_url = models.URLField(blank=True, default="https://www.instagram.com/nsukodel?utm_source=qr&igsh=MWpqaXhsMmgwb2RvMA==")
    linkedin_url = models.URLField(blank=True, default="https://linkedin.com/company/nsuk-odel")
    youtube_url = models.URLField(blank=True, default="https://youtube.com/@nsukodel")
    telegram_url = models.URLField(blank=True, default="https://t.me/nsukodel")
    
    # External portals
    student_portal_url = models.URLField(default="https://ug.nsuk.edu.ng/login/")
    application_portal_url = models.URLField(default="https://ug.nsuk.edu.ng/application/#/")
    pgd_application_url = models.URLField(default="https://pg.nsuk.edu.ng/application/#/")
    lms_portal_url = models.URLField(default="https://lms.nsuk.edu.ng/")
    library_portal_url = models.URLField(default="https://nsuk.edu.ng/library/")
    
    # Leadership messages
    vc_name = models.CharField(max_length=200, default="Prof. Sa'adatu Hassan Liman, FELLOW: ASAS, FIPMA, FICA, FHEA(UK)")
    vc_title = models.CharField(max_length=200, default="Vice-Chancellor, Nasarawa State University, Keffi")
    vc_image = models.ImageField(upload_to="leadership/", blank=True, null=True)
    vc_message = models.TextField(
        default=(
            "It gives me great pleasure to welcome you to the Directorate of Open, Distance, and e-Learning (ODeL) "
            "at Nasarawa State University, Keffi (NSUK). In today's dynamic and interconnected world, access to quality "
            "higher education is a fundamental driver of personal advancement and national socio-economic transformation.\n\n"
            "Our distance learning center embodies our commitment to breaking geographical barriers, enabling students, "
            "working professionals, and lifelong learners across Nigeria and beyond to achieve recognized degrees with unmatched "
            "flexibility, rigorous academic standards, and state-of-the-art digital infrastructure."
        )
    )
    
    director_name = models.CharField(max_length=200, default="Prof. Muhammad Haruna")
    director_title = models.CharField(max_length=200, default="Director, Directorate of Open, Distance and e-Learning")
    director_image = models.ImageField(upload_to="leadership/", blank=True, null=True)
    director_message = models.TextField(
        default=(
            "Welcome to NSUK ODeL. Our mission is to democratize higher education by leveraging cutting-edge educational "
            "technologies, robust learning management systems (LMS), and interactive pedagogy.\n\n"
            "Whether you are looking to advance your career with our pioneer B.Sc Public Administration program or prepare for "
            "our upcoming degree programs, NSUK ODeL offers a seamless blend of self-paced digital study and tutor-guided sessions."
        )
    )
    
    # History & About
    university_history = models.TextField(
        default=(
            "Nasarawa State University, Keffi was established in 2001 under the Nasarawa State Law No. 2 of 2001 as passed "
            "by the State House of Assembly. The university was founded upon the philosophy of 'belief in excellence, creativity, "
            "productivity and freedom of conscience for the advancement of individual and humanity.' The mandate of the "
            "university is to pursue and foster 'knowledge for development'.\n\n"
            "In line with the vision, thoughts, and aspirations of the founding fathers, the Directorate of Open, Distance, "
            "and e-Learning (ODeL) was established with full approval by the National Universities Commission (NUC) to expand "
            "access to world-class university education for all qualifying candidates irrespective of location."
        )
    )
    
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"{self.center_acronym} Configuration"

    @classmethod
    def get_settings(cls):
        setting, created = cls.objects.get_or_create(pk=1)
        return setting


class HeroSlide(models.Model):
    """Banners displayed on the homepage slider."""
    title = models.CharField(max_length=255)
    subtitle = models.TextField(blank=True)
    badge_text = models.CharField(max_length=100, blank=True, default="NUC Approved")
    image = models.ImageField(upload_to="banners/", blank=True, null=True)
    image_url_fallback = models.URLField(blank=True, help_text="Fallback external URL if image not uploaded")
    cta_primary_text = models.CharField(max_length=100, default="Apply Now")
    cta_primary_url = models.CharField(max_length=300, default="/admissions/how-to-apply/")
    cta_secondary_text = models.CharField(max_length=100, blank=True, default="Explore Programs")
    cta_secondary_url = models.CharField(max_length=300, blank=True, default="/programs/")
    display_order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slides"

    def __str__(self):
        return self.title

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        if self.image_url_fallback:
            return self.image_url_fallback
        return "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1600&q=80"


class Program(models.Model):
    """Academic programs offered by the ODeL Directorate."""
    DEGREE_CHOICES = [
        ('B.Sc', 'Bachelor of Science (B.Sc)'),
        ('PGD', 'Postgraduate Diploma (PGD)'),
        ('M.Sc', 'Master of Science (M.Sc)'),
        ('Cert', 'Certificate Course'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active / Enrolling'),
        ('Upcoming', 'Proposed / Upcoming (Approved)'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    degree_type = models.CharField(max_length=20, choices=DEGREE_CHOICES, default='B.Sc')
    faculty = models.CharField(max_length=200, default="Faculty of Administration")
    department = models.CharField(max_length=200, default="Department of Public Administration")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    duration = models.CharField(max_length=150, default="2 - 4 Years (Flexible Semesters)")
    
    short_description = models.TextField(help_text="Summary for cards and snippets")
    full_overview = models.TextField(help_text="Detailed description of the program")
    
    # Admission requirements
    utme_requirements = models.TextField(
        default="5 O'Level credits including English Language, Mathematics, Government/History and any other two relevant subjects."
    )
    direct_entry_requirements = models.TextField(
        default="National Diploma (ND) or NCE with minimum Upper Credit in Public Administration, Local Government, or related disciplines."
    )
    conversion_requirements = models.TextField(
        default="HND or First Degree in relevant disciplines for 300 Level Entry (2-Year Fast-track Duration)."
    )
    
    career_opportunities = models.TextField(
        blank=True,
        default="Civil Service, Public Policy Analysis, Local Government Administration, Non-Governmental Organizations (NGOs), Corporate Governance, International Relations."
    )
    
    featured_image = models.ImageField(upload_to="programs/", blank=True, null=True)
    featured_image_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Academic Program"
        verbose_name_plural = "Academic Programs"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.status})"

    def get_absolute_url(self):
        return reverse('program_detail', kwargs={'slug': self.slug})

    @property
    def get_image(self):
        if self.featured_image and hasattr(self.featured_image, 'url'):
            return self.featured_image.url
        if self.featured_image_url:
            return self.featured_image_url
        return "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80"


class Course(models.Model):
    """Specific course units offered under programs."""
    SEMESTER_CHOICES = [
        ('1st', 'First Semester'),
        ('2nd', 'Second Semester'),
    ]
    LEVEL_CHOICES = [
        ('100', '100 Level'),
        ('200', '200 Level'),
        ('300', '300 Level'),
        ('400', '400 Level'),
    ]

    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)
    course_code = models.CharField(max_length=20, help_text="e.g. PAD111, ECO111, ACC111")
    title = models.CharField(max_length=255)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='100')
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='1st')
    credit_units = models.PositiveSmallIntegerField(default=3)
    description = models.TextField(blank=True)
    learning_outcomes = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="courses/", blank=True, null=True)
    thumbnail_url = models.URLField(blank=True)
    lms_url = models.URLField(default="https://lms.nsuk.edu.ng/course/index.php?categoryid=522", help_text="Direct link to course on Moodle LMS")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['level', 'semester', 'course_code']
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return f"{self.course_code}: {self.title}"

    @property
    def get_thumbnail(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url
        if self.thumbnail_url:
            return self.thumbnail_url
        return "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80"


class AdmissionBatch(models.Model):
    """Admission lists / batches released by the ODeL Directorate."""
    title = models.CharField(max_length=255, default="Provisional Admission First List")
    academic_session = models.CharField(max_length=50, default="2025/2026", help_text="e.g. 2025/2026")
    publication_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Active lists are displayed on the public portal")
    description = models.TextField(blank=True, default="Candidates offered provisional admission into the NSUK ODeL degree program.")

    class Meta:
        ordering = ['-publication_date', '-id']
        verbose_name = "Admission Batch"
        verbose_name_plural = "Admission Batches"

    def __str__(self):
        return f"{self.title} ({self.academic_session})"

    @property
    def total_candidates(self):
        return self.candidates.count()


class AdmissionCandidate(models.Model):
    """Individual admitted student records."""
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('Admitted', 'Admitted'),
        ('Verified', 'Verified & Cleared'),
        ('Pending', 'Pending Documentation'),
    ]

    batch = models.ForeignKey(AdmissionBatch, on_delete=models.CASCADE, related_name='candidates')
    serial_number = models.PositiveIntegerField(default=1)
    candidate_name = models.CharField(max_length=255)
    applicant_id = models.CharField(max_length=50, unique=True, help_text="e.g. ODEL2500008")
    program = models.CharField(max_length=255, default="B.Sc Public Administration (ODEL)")
    level_of_entry = models.CharField(max_length=20, default="100", help_text="100, 200, or 300")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    state_of_origin = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Admitted')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['batch', 'serial_number', 'candidate_name']
        verbose_name = "Admission Candidate"
        verbose_name_plural = "Admission Candidates"

    def __str__(self):
        return f"{self.applicant_id} - {self.candidate_name}"


class StaffMember(models.Model):
    """Faculty, leadership, and administrative staff members."""
    CATEGORY_CHOICES = [
        ('Leadership', 'Principal Officers & Leadership'),
        ('Academic', 'Academic Staff & Course Facilitators'),
        ('Technical', 'e-Learning & Technical Support'),
        ('Administrative', 'Administrative Staff'),
    ]

    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=200, help_text="e.g. Director, LMS Administrator, Lead Facilitator")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='Academic')
    department = models.CharField(max_length=200, default="Directorate of ODeL")
    qualifications = models.CharField(max_length=255, blank=True, help_text="e.g. B.Sc, M.Sc, Ph.D, MNIM")
    biography = models.TextField(blank=True)
    photo = models.ImageField(upload_to="staff/", blank=True, null=True)
    photo_url = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    sort_order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'full_name']
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff Members"

    def __str__(self):
        return f"{self.full_name} ({self.position})"

    @property
    def get_photo(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        if self.photo_url:
            return self.photo_url
        return "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80"


class NewsEvent(models.Model):
    """News updates, announcements, and events."""
    CATEGORY_CHOICES = [
        ('Events', 'Events'),
        ('Application', 'Application & Admissions'),
        ('Announcement', 'General Announcement'),
        ('Academic', 'Academic Notice'),
    ]

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='Events')
    featured_image = models.ImageField(upload_to="news/", blank=True, null=True)
    featured_image_url = models.URLField(blank=True)
    excerpt = models.TextField(help_text="Short teaser paragraph")
    content = models.TextField(help_text="Full news article or event details")
    event_date = models.DateField(blank=True, null=True, help_text="If this is an event, the date of the event")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "News & Event"
        verbose_name_plural = "News & Events"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    @property
    def get_image(self):
        if self.featured_image and hasattr(self.featured_image, 'url'):
            return self.featured_image.url
        if self.featured_image_url:
            return self.featured_image_url
        return "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=800&q=80"


class FAQ(models.Model):
    """Frequently Asked Questions."""
    CATEGORY_CHOICES = [
        ('General', 'General Questions'),
        ('Admissions', 'Admissions & Entry'),
        ('LMS', 'LMS & CBT Examinations'),
        ('Academic', 'Academic & Duration'),
        ('Fees', 'Tuition & Payment'),
    ]

    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='General')
    sort_order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class InquiryMessage(models.Model):
    """Prospective student inquiries and contact submissions."""
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=255)
    program_of_interest = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Inquiry Message"
        verbose_name_plural = "Inquiry Messages"

    def __str__(self):
        return f"{self.full_name} - {self.subject}"
