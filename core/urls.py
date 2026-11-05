from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    
    # About Us subpages - canonical URL is /about/history/
    path('about/history/', views.history_view, name='history'),
    path('about/vice-chancellor/', views.vc_message_view, name='vc_message'),
    path('about/director/', views.director_message_view, name='director_message'),
    path('about/staff/', views.staff_directory_view, name='staff_directory'),
    
    # Programs & Courses
    path('programs/', views.programs_list_view, name='programs_list'),
    path('programs/<slug:slug>/', views.program_detail_view, name='program_detail'),
    path('courses/', views.courses_list_view, name='courses_list'),
    
    # Admissions
    path('admissions/', views.admissions_guide_view, name='admissions_guide'),
    path('admissions/how-to-apply/', views.admissions_guide_view, name='how_to_apply'),
    path('admission-list/', views.admission_list_view, name='admission_list'),
    path('api/check-admission/', views.check_admission_api, name='check_admission_api'),
    
    # News & Events
    path('news/', views.news_list_view, name='news_list'),
    path('news/<slug:slug>/', views.news_detail_view, name='news_detail'),
    
    # FAQ & Contact
    path('faq/', views.faq_view, name='faq'),
    path('contact/', views.contact_view, name='contact'),
]
