from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='dashboard_login'),
    path('logout/', views.logout_view, name='dashboard_logout'),
    path('change-password/', views.change_password_view, name='dashboard_change_password'),
    
    # Overview
    path('', views.dashboard_home, name='dashboard_home'),
    
    # Programs
    path('programs/', views.program_list_dash, name='dashboard_programs'),
    path('programs/add/', views.program_create_dash, name='dashboard_program_create'),
    path('programs/<int:pk>/edit/', views.program_edit_dash, name='dashboard_program_edit'),
    path('programs/<int:pk>/delete/', views.program_delete_dash, name='dashboard_program_delete'),
    
    # Courses
    path('courses/', views.course_list_dash, name='dashboard_courses'),
    path('courses/add/', views.course_create_dash, name='dashboard_course_create'),
    path('courses/<int:pk>/edit/', views.course_edit_dash, name='dashboard_course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete_dash, name='dashboard_course_delete'),
    
    # Admission Batches
    path('admissions/batches/', views.batch_list_dash, name='dashboard_batches'),
    path('admissions/batches/add/', views.batch_create_dash, name='dashboard_batch_create'),
    path('admissions/batches/<int:pk>/edit/', views.batch_edit_dash, name='dashboard_batch_edit'),
    path('admissions/batches/<int:pk>/delete/', views.batch_delete_dash, name='dashboard_batch_delete'),
    
    # Admission Candidates & Bulk CSV
    path('admissions/candidates/', views.candidate_list_dash, name='dashboard_candidates'),
    path('admissions/candidates/add/', views.candidate_create_dash, name='dashboard_candidate_create'),
    path('admissions/candidates/<int:pk>/edit/', views.candidate_edit_dash, name='dashboard_candidate_edit'),
    path('admissions/candidates/<int:pk>/delete/', views.candidate_delete_dash, name='dashboard_candidate_delete'),
    path('admissions/bulk-upload/', views.bulk_upload_candidates_dash, name='dashboard_bulk_upload'),
    path('admissions/sample-csv/', views.download_sample_csv, name='dashboard_sample_csv'),
    path('admissions/export-csv/', views.export_candidates_csv, name='dashboard_export_csv'),
    
    # News & Events
    path('news/', views.news_list_dash, name='dashboard_news'),
    path('news/add/', views.news_create_dash, name='dashboard_news_create'),
    path('news/<int:pk>/edit/', views.news_edit_dash, name='dashboard_news_edit'),
    path('news/<int:pk>/delete/', views.news_delete_dash, name='dashboard_news_delete'),
    
    # Staff
    path('staff/', views.staff_list_dash, name='dashboard_staff'),
    path('staff/add/', views.staff_create_dash, name='dashboard_staff_create'),
    path('staff/<int:pk>/edit/', views.staff_edit_dash, name='dashboard_staff_edit'),
    path('staff/<int:pk>/delete/', views.staff_delete_dash, name='dashboard_staff_delete'),
    
    # Hero Slides
    path('slides/', views.slide_list_dash, name='dashboard_slides'),
    path('slides/add/', views.slide_create_dash, name='dashboard_slide_create'),
    path('slides/<int:pk>/edit/', views.slide_edit_dash, name='dashboard_slide_edit'),
    path('slides/<int:pk>/delete/', views.slide_delete_dash, name='dashboard_slide_delete'),
    
    # FAQs
    path('faqs/', views.faq_list_dash, name='dashboard_faqs'),
    path('faqs/add/', views.faq_create_dash, name='dashboard_faq_create'),
    path('faqs/<int:pk>/edit/', views.faq_edit_dash, name='dashboard_faq_edit'),
    path('faqs/<int:pk>/delete/', views.faq_delete_dash, name='dashboard_faq_delete'),
    
    # Inquiries Inbox
    path('inquiries/', views.inquiry_list_dash, name='dashboard_inquiries'),
    path('inquiries/<int:pk>/', views.inquiry_detail_dash, name='dashboard_inquiry_detail'),
    path('inquiries/<int:pk>/delete/', views.inquiry_delete_dash, name='dashboard_inquiry_delete'),
    
    # Global Settings
    path('settings/', views.settings_edit_dash, name='dashboard_settings'),
]
