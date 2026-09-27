from django import forms
from core.models import (
    Program, Course, AdmissionBatch, AdmissionCandidate, 
    StaffMember, NewsEvent, HeroSlide, FAQ, SiteSetting, InquiryMessage
)

TAILWIND_INPUT = 'w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all outline-none text-sm'
TAILWIND_SELECT = 'w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all outline-none text-sm'
TAILWIND_TEXTAREA = 'w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all outline-none text-sm'
TAILWIND_CHECKBOX = 'h-5 w-5 text-sky-600 focus:ring-sky-500 border-slate-300 rounded'
TAILWIND_FILE = 'w-full text-sm text-slate-500 dark:text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-sky-50 file:text-sky-700 hover:file:bg-sky-100'


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = [
            'name', 'slug', 'degree_type', 'faculty', 'department', 'status', 
            'duration', 'short_description', 'full_overview', 'utme_requirements', 
            'direct_entry_requirements', 'conversion_requirements', 'career_opportunities', 
            'featured_image', 'featured_image_url', 'is_featured', 'is_active', 'display_order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. B.Sc Public Administration'}),
            'slug': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'b-sc-public-administration (optional)'}),
            'degree_type': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'faculty': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'department': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'status': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'duration': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. 2 - 4 Years'}),
            'short_description': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 3}),
            'full_overview': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 5}),
            'utme_requirements': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 3}),
            'direct_entry_requirements': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 3}),
            'conversion_requirements': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 3}),
            'career_opportunities': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 3}),
            'featured_image': forms.FileInput(attrs={'class': TAILWIND_FILE}),
            'featured_image_url': forms.URLInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'https://...'}),
            'is_featured': forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
            'is_active': forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
            'display_order': forms.NumberInput(attrs={'class': TAILWIND_INPUT}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'program', 'course_code', 'title', 'level', 'semester', 
            'credit_units', 'description', 'learning_outcomes', 'thumbnail', 
            'thumbnail_url', 'lms_url', 'is_active', 'display_order'
        ]
        widgets = {
            'program': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'course_code': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. PAD111'}),
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Introduction to Public Administration I'}),
            'level': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'semester': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'credit_units': forms.NumberInput(attrs={'class': TAILWIND_INPUT}),
            'description': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 4}),
            'learning_outcomes': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 3}),
            'thumbnail': forms.FileInput(attrs={'class': TAILWIND_FILE}),
            'thumbnail_url': forms.URLInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'https://...'}),
            'lms_url': forms.URLInput(attrs={'class': TAILWIND_INPUT}),
            'is_active': forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
            'display_order': forms.NumberInput(attrs={'class': TAILWIND_INPUT}),
        }


class AdmissionBatchForm(forms.ModelForm):
    class Meta:
        model = AdmissionBatch
        fields = ['title', 'academic_session', 'is_active', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Provisional Admission First List'}),
            'academic_session': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. 2025/2026'}),
            'is_active': forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
            'description': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 3}),
        }


class AdmissionCandidateForm(forms.ModelForm):
    class Meta:
        model = AdmissionCandidate
        fields = [
            'batch', 'serial_number', 'candidate_name', 'applicant_id', 
            'program', 'level_of_entry', 'gender', 'state_of_origin', 'status'
        ]
        widgets = {
            'batch': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'serial_number': forms.NumberInput(attrs={'class': TAILWIND_INPUT}),
            'candidate_name': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. LUKMAN Muhammed Sani'}),
            'applicant_id': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. ODEL2500008'}),
            'program': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. B.Sc Public Administration (ODEL)'}),
            'level_of_entry': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': '100, 200, or 300'}),
            'gender': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'state_of_origin': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'e.g. Nasarawa'}),
            'status': forms.Select(attrs={'class': TAILWIND_SELECT}),
        }


class BulkAdmissionCSVForm(forms.Form):
    batch = forms.ModelChoiceField(
        queryset=AdmissionBatch.objects.all(),
        widget=forms.Select(attrs={'class': TAILWIND_SELECT}),
        help_text="Select which batch/list these candidates will be imported into"
    )
    csv_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': TAILWIND_FILE, 'accept': '.csv'}),
        help_text="Upload a .csv file containing columns: S/N, NAME, APPLICANT ID, PROGRAM, LEVEL OF ENTRY, SEX, STATE"
    )
    overwrite_existing = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
        help_text="Update details if an applicant ID already exists"
    )


class StaffMemberForm(forms.ModelForm):
    class Meta:
        model = StaffMember
        fields = [
            'full_name', 'position', 'category', 'department', 
            'qualifications', 'biography', 'photo', 'photo_url', 
            'email', 'phone', 'sort_order', 'is_active'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'position': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'category': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'department': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'qualifications': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'biography': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 4}),
            'photo': forms.FileInput(attrs={'class': TAILWIND_FILE}),
            'photo_url': forms.URLInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'https://...'}),
            'email': forms.EmailInput(attrs={'class': TAILWIND_INPUT}),
            'phone': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'sort_order': forms.NumberInput(attrs={'class': TAILWIND_INPUT}),
            'is_active': forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
        }


class NewsEventForm(forms.ModelForm):
    class Meta:
        model = NewsEvent
        fields = [
            'title', 'slug', 'category', 'featured_image', 'featured_image_url', 
            'excerpt', 'content', 'event_date', 'is_featured', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'slug': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'Leave blank to auto-generate'}),
            'category': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'featured_image': forms.FileInput(attrs={'class': TAILWIND_FILE}),
            'featured_image_url': forms.URLInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'https://...'}),
            'excerpt': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 3}),
            'content': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 8}),
            'event_date': forms.DateInput(attrs={'class': TAILWIND_INPUT, 'type': 'date'}),
            'is_featured': forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
            'is_active': forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
        }


class HeroSlideForm(forms.ModelForm):
    class Meta:
        model = HeroSlide
        fields = [
            'title', 'subtitle', 'badge_text', 'image', 'image_url_fallback', 
            'cta_primary_text', 'cta_primary_url', 'cta_secondary_text', 
            'cta_secondary_url', 'display_order', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'subtitle': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 2}),
            'badge_text': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'image': forms.FileInput(attrs={'class': TAILWIND_FILE}),
            'image_url_fallback': forms.URLInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'https://...'}),
            'cta_primary_text': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'cta_primary_url': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'cta_secondary_text': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'cta_secondary_url': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'display_order': forms.NumberInput(attrs={'class': TAILWIND_INPUT}),
            'is_active': forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
        }


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'category', 'sort_order', 'is_active']
        widgets = {
            'question': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'answer': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 4}),
            'category': forms.Select(attrs={'class': TAILWIND_SELECT}),
            'sort_order': forms.NumberInput(attrs={'class': TAILWIND_INPUT}),
            'is_active': forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
        }


class SiteSettingForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = [
            'site_name', 'center_name', 'center_acronym', 'top_announcement', 'tagline',
            'contact_email', 'contact_phone_1', 'contact_phone_2', 'whatsapp_number', 'address',
            'facebook_url', 'twitter_x_url', 'instagram_url', 'linkedin_url', 'youtube_url', 'telegram_url',
            'student_portal_url', 'application_portal_url', 'pgd_application_url', 'lms_portal_url', 'library_portal_url',
            'vc_name', 'vc_title', 'vc_image', 'vc_message',
            'director_name', 'director_title', 'director_image', 'director_message',
            'university_history'
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'center_name': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'center_acronym': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'top_announcement': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'tagline': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'contact_email': forms.EmailInput(attrs={'class': TAILWIND_INPUT}),
            'contact_phone_1': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'contact_phone_2': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'whatsapp_number': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'address': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 2}),
            'facebook_url': forms.URLInput(attrs={'class': TAILWIND_INPUT}),
            'twitter_x_url': forms.URLInput(attrs={'class': TAILWIND_INPUT}),
            'instagram_url': forms.URLInput(attrs={'class': TAILWIND_INPUT}),
            'linkedin_url': forms.URLInput(attrs={'class': TAILWIND_INPUT}),
            'youtube_url': forms.URLInput(attrs={'class': TAILWIND_INPUT}),
            'telegram_url': forms.URLInput(attrs={'class': TAILWIND_INPUT}),
            'student_portal_url': forms.URLInput(attrs={'class': TAILWIND_INPUT}),
            'application_portal_url': forms.URLInput(attrs={'class': TAILWIND_INPUT}),
            'pgd_application_url': forms.URLInput(attrs={'class': TAILWIND_INPUT}),
            'lms_portal_url': forms.URLInput(attrs={'class': TAILWIND_INPUT}),
            'library_portal_url': forms.URLInput(attrs={'class': TAILWIND_INPUT}),
            'vc_name': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'vc_title': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'vc_image': forms.FileInput(attrs={'class': TAILWIND_FILE}),
            'vc_message': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 6}),
            'director_name': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'director_title': forms.TextInput(attrs={'class': TAILWIND_INPUT}),
            'director_image': forms.FileInput(attrs={'class': TAILWIND_FILE}),
            'director_message': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 6}),
            'university_history': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 6}),
        }


class InquiryResponseForm(forms.ModelForm):
    class Meta:
        model = InquiryMessage
        fields = ['is_resolved', 'admin_notes']
        widgets = {
            'is_resolved': forms.CheckboxInput(attrs={'class': TAILWIND_CHECKBOX}),
            'admin_notes': forms.Textarea(attrs={'class': TAILWIND_TEXTAREA, 'rows': 4, 'placeholder': 'Internal notes or record of resolution...'}),
        }
