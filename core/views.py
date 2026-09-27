import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import (
    SiteSetting, HeroSlide, Program, Course, AdmissionBatch, 
    AdmissionCandidate, StaffMember, NewsEvent, FAQ, InquiryMessage
)
from .forms import ContactInquiryForm


def index(request):
    """Homepage view mirroring odel.nsuk.edu.ng with enhanced modern UI."""
    slides = HeroSlide.objects.filter(is_active=True)
    featured_programs = Program.objects.filter(is_active=True, is_featured=True)[:6]
    featured_courses = Course.objects.filter(is_active=True)[:6]
    events = NewsEvent.objects.filter(is_active=True)[:4]
    faqs = FAQ.objects.filter(is_active=True)[:6]
    latest_batch = AdmissionBatch.objects.filter(is_active=True).first()
    settings = SiteSetting.get_settings()

    context = {
        'slides': slides,
        'featured_programs': featured_programs,
        'featured_courses': featured_courses,
        'events': events,
        'faqs': faqs,
        'latest_batch': latest_batch,
        'settings': settings,
    }
    return render(request, 'core/index.html', context)


def history_view(request):
    """ODeL History, vision, and institutional background."""
    settings = SiteSetting.get_settings()
    return render(request, 'core/history.html', {'settings': settings})


def vc_message_view(request):
    """Vice-Chancellor's official address."""
    settings = SiteSetting.get_settings()
    return render(request, 'core/vc_message.html', {'settings': settings})


def director_message_view(request):
    """Director's official welcome message."""
    settings = SiteSetting.get_settings()
    return render(request, 'core/director_message.html', {'settings': settings})


def staff_directory_view(request):
    """Directory of ODeL leadership, academic facilitators, and staff."""
    category = request.GET.get('category', 'all')
    staff_qs = StaffMember.objects.filter(is_active=True)
    
    if category != 'all':
        staff_qs = staff_qs.filter(category=category)
        
    context = {
        'staff_members': staff_qs,
        'selected_category': category,
        'categories': StaffMember.CATEGORY_CHOICES,
    }
    return render(request, 'core/staff.html', context)


def programs_list_view(request):
    """Catalog of all degree programs (active and upcoming)."""
    active_programs = Program.objects.filter(is_active=True, status='Active')
    upcoming_programs = Program.objects.filter(is_active=True, status='Upcoming')
    
    context = {
        'active_programs': active_programs,
        'upcoming_programs': upcoming_programs,
    }
    return render(request, 'core/programs.html', context)


def program_detail_view(request, slug):
    """Detailed view for a specific program (e.g. B.Sc Public Administration)."""
    program = get_object_or_404(Program, slug=slug, is_active=True)
    courses = program.courses.filter(is_active=True)
    return render(request, 'core/program_detail.html', {
        'program': program,
        'courses': courses,
    })


def courses_list_view(request):
    """Searchable and filterable course catalog."""
    query = request.GET.get('q', '').strip()
    level = request.GET.get('level', '')
    semester = request.GET.get('semester', '')
    
    courses_qs = Course.objects.filter(is_active=True)
    
    if query:
        courses_qs = courses_qs.filter(
            Q(course_code__icontains=query) |
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    if level:
        courses_qs = courses_qs.filter(level=level)
    if semester:
        courses_qs = courses_qs.filter(semester=semester)
        
    paginator = Paginator(courses_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_level': level,
        'selected_semester': semester,
        'total_count': courses_qs.count(),
    }
    return render(request, 'core/courses.html', context)


def admission_list_view(request):
    """
    Live Admission List portal matching and enhancing odel.nsuk.edu.ng/admission-list/
    Supports real-time search, batch switching, level/gender/state filtering, and pagination.
    """
    batch_id = request.GET.get('batch')
    query = request.GET.get('q', '').strip()
    level = request.GET.get('level', '').strip()
    gender = request.GET.get('gender', '').strip()
    state = request.GET.get('state', '').strip()
    
    batches = AdmissionBatch.objects.filter(is_active=True)
    
    if batch_id:
        selected_batch = get_object_or_404(AdmissionBatch, id=batch_id, is_active=True)
    else:
        selected_batch = batches.first()
        
    candidates_qs = AdmissionCandidate.objects.none()
    
    if selected_batch:
        candidates_qs = selected_batch.candidates.all()
        if query:
            candidates_qs = candidates_qs.filter(
                Q(applicant_id__icontains=query) |
                Q(candidate_name__icontains=query) |
                Q(state_of_origin__icontains=query) |
                Q(program__icontains=query)
            )
        if level:
            candidates_qs = candidates_qs.filter(level_of_entry=level)
        if gender:
            candidates_qs = candidates_qs.filter(gender=gender)
        if state:
            candidates_qs = candidates_qs.filter(state_of_origin__iexact=state)

    # Distinct states for filter dropdown
    available_states = []
    if selected_batch:
        available_states = sorted(list(set(
            selected_batch.candidates.exclude(state_of_origin='').values_list('state_of_origin', flat=True)
        )))

    paginator = Paginator(candidates_qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'batches': batches,
        'selected_batch': selected_batch,
        'page_obj': page_obj,
        'query': query,
        'selected_level': level,
        'selected_gender': gender,
        'selected_state': state,
        'available_states': available_states,
        'total_count': candidates_qs.count() if selected_batch else 0,
    }
    return render(request, 'core/admission_list.html', context)


def check_admission_api(request):
    """Quick API for student admission verification modal."""
    applicant_id = request.GET.get('applicant_id', '').strip()
    if not applicant_id:
        return JsonResponse({'status': 'error', 'message': 'Please provide an Applicant ID.'})
    
    candidate = AdmissionCandidate.objects.filter(applicant_id__iexact=applicant_id).select_related('batch').first()
    if candidate:
        return JsonResponse({
            'status': 'success',
            'found': True,
            'candidate': {
                'name': candidate.candidate_name,
                'applicant_id': candidate.applicant_id,
                'program': candidate.program,
                'level': candidate.level_of_entry,
                'gender': candidate.gender,
                'state': candidate.state_of_origin or 'N/A',
                'batch': candidate.batch.title,
                'session': candidate.batch.academic_session,
                'admission_status': candidate.status,
            }
        })
    else:
        return JsonResponse({
            'status': 'success',
            'found': False,
            'message': f'No admission record found for Applicant ID: {applicant_id}. Please double check or contact ODeL support.'
        })


def admissions_guide_view(request):
    """How to apply, requirements, duration and application portals."""
    settings = SiteSetting.get_settings()
    programs = Program.objects.filter(is_active=True)
    return render(request, 'core/admissions_guide.html', {
        'settings': settings,
        'programs': programs,
    })


def faq_view(request):
    """Interactive FAQs with category filters and search."""
    faqs = FAQ.objects.filter(is_active=True)
    categories = FAQ.CATEGORY_CHOICES
    return render(request, 'core/faq.html', {
        'faqs': faqs,
        'categories': categories,
    })


def contact_view(request):
    """Contact us page with dynamic form submission."""
    settings = SiteSetting.get_settings()
    if request.method == 'POST':
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            messages.success(
                request, 
                "Thank you for contacting NSUK ODeL! Your message has been received and our admissions support team will respond shortly."
            )
            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors in the form below.")
    else:
        form = ContactInquiryForm()
        
    return render(request, 'core/contact.html', {
        'form': form,
        'settings': settings,
    })


def news_list_view(request):
    """All news, events, and announcements."""
    category = request.GET.get('category', '')
    news_qs = NewsEvent.objects.filter(is_active=True)
    
    if category:
        news_qs = news_qs.filter(category=category)
        
    paginator = Paginator(news_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/news_list.html', {
        'page_obj': page_obj,
        'selected_category': category,
        'categories': NewsEvent.CATEGORY_CHOICES,
    })


def news_detail_view(request, slug):
    """Single news or event article."""
    article = get_object_or_404(NewsEvent, slug=slug, is_active=True)
    recent_news = NewsEvent.objects.filter(is_active=True).exclude(id=article.id)[:4]
    return render(request, 'core/news_detail.html', {
        'article': article,
        'recent_news': recent_news,
    })
