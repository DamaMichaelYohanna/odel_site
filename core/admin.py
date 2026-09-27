from django.contrib import admin
from .models import (
    SiteSetting, HeroSlide, Program, Course, AdmissionBatch, 
    AdmissionCandidate, StaffMember, NewsEvent, FAQ, InquiryMessage
)

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'center_acronym', 'contact_phone_1', 'contact_email')

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge_text', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'degree_type', 'faculty', 'status', 'is_active', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('degree_type', 'status', 'is_active')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'title', 'program', 'level', 'semester', 'credit_units', 'is_active')
    list_filter = ('level', 'semester', 'program', 'is_active')
    search_fields = ('course_code', 'title')

@admin.register(AdmissionBatch)
class AdmissionBatchAdmin(admin.ModelAdmin):
    list_display = ('title', 'academic_session', 'publication_date', 'is_active', 'total_candidates')
    list_filter = ('academic_session', 'is_active')

@admin.register(AdmissionCandidate)
class AdmissionCandidateAdmin(admin.ModelAdmin):
    list_display = ('applicant_id', 'candidate_name', 'level_of_entry', 'gender', 'state_of_origin', 'batch', 'status')
    list_filter = ('batch', 'level_of_entry', 'gender', 'status')
    search_fields = ('applicant_id', 'candidate_name', 'state_of_origin')

@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'category', 'email', 'sort_order', 'is_active')
    list_filter = ('category', 'is_active')

@admin.register(NewsEvent)
class NewsEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'event_date', 'is_featured', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category', 'is_featured', 'is_active')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'sort_order', 'is_active')
    list_filter = ('category', 'is_active')
    list_editable = ('sort_order', 'is_active')

@admin.register(InquiryMessage)
class InquiryMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'program_of_interest', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('full_name', 'email', 'subject', 'message')
