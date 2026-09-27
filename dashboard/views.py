import csv
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.urls import reverse

from core.models import (
    Program, Course, AdmissionBatch, AdmissionCandidate, 
    StaffMember, NewsEvent, HeroSlide, FAQ, SiteSetting, InquiryMessage
)
from .forms import (
    ProgramForm, CourseForm, AdmissionBatchForm, AdmissionCandidateForm, 
    BulkAdmissionCSVForm, StaffMemberForm, NewsEventForm, HeroSlideForm, 
    FAQForm, SiteSettingForm, InquiryResponseForm
)


# --- AUTHENTICATION VIEWS ---

def login_view(request):
    """Admin/Staff dashboard login."""
    if request.user.is_authenticated:
        return redirect('dashboard_home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            next_url = request.GET.get('next', 'dashboard_home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'dashboard/auth/login.html', {'form': form})


def logout_view(request):
    """Admin logout."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('dashboard_login')


@login_required
def change_password_view(request):
    """Admin password update."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect('dashboard_home')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/auth/change_password.html', {'form': form})


# --- DASHBOARD HOME ---

@login_required
def dashboard_home(request):
    """Overview hub with statistics, quick actions, and recent activity."""
    total_candidates = AdmissionCandidate.objects.count()
    total_programs = Program.objects.count()
    total_courses = Course.objects.count()
    total_staff = StaffMember.objects.count()
    total_news = NewsEvent.objects.count()
    total_faqs = FAQ.objects.count()
    total_inquiries = InquiryMessage.objects.count()
    pending_inquiries = InquiryMessage.objects.filter(is_resolved=False).count()
    
    recent_candidates = AdmissionCandidate.objects.select_related('batch').order_by('-created_at')[:8]
    recent_inquiries = InquiryMessage.objects.order_by('-created_at')[:5]
    batches = AdmissionBatch.objects.annotate(candidate_count=Count('candidates'))
    
    context = {
        'total_candidates': total_candidates,
        'total_programs': total_programs,
        'total_courses': total_courses,
        'total_staff': total_staff,
        'total_news': total_news,
        'total_faqs': total_faqs,
        'total_inquiries': total_inquiries,
        'pending_inquiries': pending_inquiries,
        'recent_candidates': recent_candidates,
        'recent_inquiries': recent_inquiries,
        'batches': batches,
    }
    return render(request, 'dashboard/index.html', context)


# --- PROGRAMS MANAGEMENT ---

@login_required
def program_list_dash(request):
    programs = Program.objects.all().order_by('display_order', 'name')
    return render(request, 'dashboard/programs/list.html', {'programs': programs})


@login_required
def program_create_dash(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES)
        if form.is_valid():
            program = form.save()
            messages.success(request, f"Program '{program.name}' created successfully!")
            return redirect('dashboard_programs')
    else:
        form = ProgramForm()
    return render(request, 'dashboard/programs/form.html', {'form': form, 'title': 'Add Academic Program'})


@login_required
def program_edit_dash(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, f"Program '{program.name}' updated successfully!")
            return redirect('dashboard_programs')
    else:
        form = ProgramForm(instance=program)
    return render(request, 'dashboard/programs/form.html', {'form': form, 'title': f'Edit Program: {program.name}', 'program': program})


@login_required
def program_delete_dash(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        name = program.name
        program.delete()
        messages.success(request, f"Program '{name}' deleted.")
        return redirect('dashboard_programs')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': f"Program: {program.name}",
        'cancel_url': reverse('dashboard_programs')
    })


# --- COURSES MANAGEMENT ---

@login_required
def course_list_dash(request):
    query = request.GET.get('q', '').strip()
    level = request.GET.get('level', '')
    courses_qs = Course.objects.select_related('program').all()
    
    if query:
        courses_qs = courses_qs.filter(
            Q(course_code__icontains=query) |
            Q(title__icontains=query)
        )
    if level:
        courses_qs = courses_qs.filter(level=level)
        
    paginator = Paginator(courses_qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/courses/list.html', {
        'page_obj': page_obj,
        'query': query,
        'selected_level': level,
        'total_count': courses_qs.count()
    })


@login_required
def course_create_dash(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            messages.success(request, f"Course '{course.course_code}: {course.title}' created successfully!")
            return redirect('dashboard_courses')
    else:
        form = CourseForm()
    return render(request, 'dashboard/courses/form.html', {'form': form, 'title': 'Add Course'})


@login_required
def course_edit_dash(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course '{course.course_code}' updated successfully!")
            return redirect('dashboard_courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'dashboard/courses/form.html', {'form': form, 'title': f'Edit Course: {course.course_code}', 'course': course})


@login_required
def course_delete_dash(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        code = course.course_code
        course.delete()
        messages.success(request, f"Course '{code}' deleted.")
        return redirect('dashboard_courses')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': f"Course: {course.course_code} - {course.title}",
        'cancel_url': reverse('dashboard_courses')
    })


# --- ADMISSION LISTS MANAGEMENT ---

@login_required
def batch_list_dash(request):
    batches = AdmissionBatch.objects.annotate(candidate_count=Count('candidates')).order_by('-publication_date')
    return render(request, 'dashboard/admissions/batches.html', {'batches': batches})


@login_required
def batch_create_dash(request):
    if request.method == 'POST':
        form = AdmissionBatchForm(request.POST)
        if form.is_valid():
            batch = form.save()
            messages.success(request, f"Admission Batch '{batch.title}' created!")
            return redirect('dashboard_batches')
    else:
        form = AdmissionBatchForm()
    return render(request, 'dashboard/admissions/batch_form.html', {'form': form, 'title': 'Create Admission Batch'})


@login_required
def batch_edit_dash(request, pk):
    batch = get_object_or_404(AdmissionBatch, pk=pk)
    if request.method == 'POST':
        form = AdmissionBatchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            messages.success(request, f"Admission Batch '{batch.title}' updated!")
            return redirect('dashboard_batches')
    else:
        form = AdmissionBatchForm(instance=batch)
    return render(request, 'dashboard/admissions/batch_form.html', {'form': form, 'title': f'Edit Batch: {batch.title}', 'batch': batch})


@login_required
def batch_delete_dash(request, pk):
    batch = get_object_or_404(AdmissionBatch, pk=pk)
    if request.method == 'POST':
        title = batch.title
        batch.delete()
        messages.success(request, f"Admission Batch '{title}' and all associated candidates deleted.")
        return redirect('dashboard_batches')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': f"Admission Batch: {batch.title} ({batch.candidates.count()} candidates)",
        'cancel_url': reverse('dashboard_batches')
    })


@login_required
def candidate_list_dash(request):
    """Manage individual candidate records with search, filter, and bulk upload button."""
    batch_id = request.GET.get('batch')
    query = request.GET.get('q', '').strip()
    level = request.GET.get('level', '')
    gender = request.GET.get('gender', '')
    state = request.GET.get('state', '')
    
    batches = AdmissionBatch.objects.all()
    candidates_qs = AdmissionCandidate.objects.select_related('batch').all()
    
    if batch_id:
        candidates_qs = candidates_qs.filter(batch_id=batch_id)
    if query:
        candidates_qs = candidates_qs.filter(
            Q(applicant_id__icontains=query) |
            Q(candidate_name__icontains=query) |
            Q(state_of_origin__icontains=query)
        )
    if level:
        candidates_qs = candidates_qs.filter(level_of_entry=level)
    if gender:
        candidates_qs = candidates_qs.filter(gender=gender)
    if state:
        candidates_qs = candidates_qs.filter(state_of_origin__iexact=state)
        
    paginator = Paginator(candidates_qs, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/admissions/candidate_list.html', {
        'page_obj': page_obj,
        'batches': batches,
        'selected_batch_id': batch_id,
        'query': query,
        'selected_level': level,
        'selected_gender': gender,
        'selected_state': state,
        'total_count': candidates_qs.count()
    })


@login_required
def candidate_create_dash(request):
    if request.method == 'POST':
        form = AdmissionCandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save()
            messages.success(request, f"Admitted candidate '{candidate.candidate_name}' ({candidate.applicant_id}) added!")
            return redirect('dashboard_candidates')
    else:
        form = AdmissionCandidateForm()
    return render(request, 'dashboard/admissions/candidate_form.html', {'form': form, 'title': 'Add Admitted Student'})


@login_required
def candidate_edit_dash(request, pk):
    candidate = get_object_or_404(AdmissionCandidate, pk=pk)
    if request.method == 'POST':
        form = AdmissionCandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, f"Candidate '{candidate.applicant_id}' updated!")
            return redirect('dashboard_candidates')
    else:
        form = AdmissionCandidateForm(instance=candidate)
    return render(request, 'dashboard/admissions/candidate_form.html', {'form': form, 'title': f'Edit Candidate: {candidate.applicant_id}', 'candidate': candidate})


@login_required
def candidate_delete_dash(request, pk):
    candidate = get_object_or_404(AdmissionCandidate, pk=pk)
    if request.method == 'POST':
        app_id = candidate.applicant_id
        candidate.delete()
        messages.success(request, f"Candidate '{app_id}' deleted.")
        return redirect('dashboard_candidates')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': f"Candidate: {candidate.applicant_id} - {candidate.candidate_name}",
        'cancel_url': reverse('dashboard_candidates')
    })


@login_required
def bulk_upload_candidates_dash(request):
    """
    Bulk CSV importer for admission lists.
    Parses CSV with standard headers: S/N, NAME, APPLICANT ID, PROGRAM, LEVEL OF ENTRY, SEX, STATE
    """
    if request.method == 'POST':
        form = BulkAdmissionCSVForm(request.POST, request.FILES)
        if form.is_valid():
            batch = form.cleaned_data['batch']
            csv_file = form.cleaned_data['csv_file']
            overwrite = form.cleaned_data['overwrite_existing']
            
            try:
                decoded_file = csv_file.read().decode('utf-8-sig', errors='replace')
                io_string = io.StringIO(decoded_file)
                reader = csv.reader(io_string)
                
                rows = [row for row in reader if any(field.strip() for field in row)]
                if not rows:
                    messages.error(request, "The uploaded CSV file is empty.")
                    return redirect('dashboard_bulk_upload')
                
                # Identify header row
                header_idx = -1
                for idx, row in enumerate(rows):
                    row_upper = [c.upper().strip() for c in row]
                    if any('APPLICANT' in c or 'ID' in c for c in row_upper) and any('NAME' in c for c in row_upper):
                        header_idx = idx
                        break
                
                if header_idx == -1:
                    # Treat first row as header
                    header_idx = 0
                
                headers = [h.strip().upper() for h in rows[header_idx]]
                
                # Map column indices
                col_map = {
                    'sn': -1,
                    'name': -1,
                    'applicant_id': -1,
                    'program': -1,
                    'level': -1,
                    'gender': -1,
                    'state': -1
                }
                
                for idx, h in enumerate(headers):
                    if 'S/N' in h or h == 'SN' or 'SERIAL' in h:
                        col_map['sn'] = idx
                    elif 'NAME' in h:
                        col_map['name'] = idx
                    elif 'APPLICANT' in h or 'REG' in h or 'ID' in h:
                        col_map['applicant_id'] = idx
                    elif 'PROGRAM' in h or 'COURSE' in h:
                        col_map['program'] = idx
                    elif 'LEVEL' in h or 'ENTRY' in h:
                        col_map['level'] = idx
                    elif 'SEX' in h or 'GENDER' in h:
                        col_map['gender'] = idx
                    elif 'STATE' in h:
                        col_map['state'] = idx

                # Fallbacks if headers weren't named standardly
                if col_map['applicant_id'] == -1 and len(headers) > 2:
                    col_map['sn'] = 0
                    col_map['name'] = 1
                    col_map['applicant_id'] = 2
                    col_map['program'] = 3
                    col_map['level'] = 4
                    col_map['gender'] = 5
                    col_map['state'] = 6

                data_rows = rows[header_idx + 1:]
                created_count = 0
                updated_count = 0
                errors = []

                for row_num, row in enumerate(data_rows, start=header_idx + 2):
                    if not row or not any(field.strip() for field in row):
                        continue
                    
                    app_id = row[col_map['applicant_id']].strip() if col_map['applicant_id'] < len(row) and col_map['applicant_id'] != -1 else ''
                    name = row[col_map['name']].strip() if col_map['name'] < len(row) and col_map['name'] != -1 else ''
                    
                    if not app_id and not name:
                        continue
                        
                    if not app_id:
                        errors.append(f"Row {row_num}: Missing Applicant ID for '{name}'")
                        continue

                    # Extract fields with safe fallbacks
                    sn_val = 1
                    if col_map['sn'] != -1 and col_map['sn'] < len(row):
                        try:
                            sn_val = int(row[col_map['sn']].strip())
                        except ValueError:
                            sn_val = created_count + updated_count + 1
                    else:
                        sn_val = created_count + updated_count + 1
                        
                    prog_val = row[col_map['program']].strip() if col_map['program'] != -1 and col_map['program'] < len(row) else 'B.Sc Public Administration (ODEL)'
                    if not prog_val:
                        prog_val = 'B.Sc Public Administration (ODEL)'
                        
                    lvl_val = row[col_map['level']].strip() if col_map['level'] != -1 and col_map['level'] < len(row) else '100'
                    if not lvl_val:
                        lvl_val = '100'
                        
                    gender_raw = row[col_map['gender']].strip() if col_map['gender'] != -1 and col_map['gender'] < len(row) else 'Male'
                    gender_val = 'Female' if gender_raw.lower().startswith('f') else 'Male'
                    
                    state_val = row[col_map['state']].strip() if col_map['state'] != -1 and col_map['state'] < len(row) else ''

                    existing = AdmissionCandidate.objects.filter(applicant_id__iexact=app_id).first()
                    if existing:
                        if overwrite:
                            existing.batch = batch
                            existing.serial_number = sn_val
                            existing.candidate_name = name or existing.candidate_name
                            existing.program = prog_val
                            existing.level_of_entry = lvl_val
                            existing.gender = gender_val
                            existing.state_of_origin = state_val
                            existing.save()
                            updated_count += 1
                    else:
                        AdmissionCandidate.objects.create(
                            batch=batch,
                            serial_number=sn_val,
                            candidate_name=name,
                            applicant_id=app_id,
                            program=prog_val,
                            level_of_entry=lvl_val,
                            gender=gender_val,
                            state_of_origin=state_val,
                            status='Admitted'
                        )
                        created_count += 1

                msg = f"Bulk Import Completed! Added: {created_count} candidates, Updated: {updated_count} candidates into '{batch.title}'."
                if errors:
                    msg += f" (Encountered {len(errors)} issues: {'; '.join(errors[:3])})"
                messages.success(request, msg)
                return redirect('dashboard_candidates')

            except Exception as e:
                messages.error(request, f"Error processing CSV: {str(e)}")
    else:
        form = BulkAdmissionCSVForm()
        
    return render(request, 'dashboard/admissions/bulk_upload.html', {'form': form})


@login_required
def download_sample_csv(request):
    """Generates a sample CSV template for staff download."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="NSUK_ODeL_Admission_Sample.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['S/N', 'NAME', 'APPLICANT ID', 'PROGRAM', 'LEVEL OF ENTRY', 'SEX', 'STATE'])
    writer.writerow([1, 'LUKMAN Muhammed Sani', 'ODEL2500008', 'B.Sc Public Administration (ODEL)', '100', 'Male', 'Nasarawa'])
    writer.writerow([2, 'IKPE Bright Dooshima', 'ODEL2500209', 'B.Sc Public Administration (ODEL)', '100', 'Female', 'Cross River'])
    writer.writerow([3, 'FABEKE Douglas Deeka', 'ODEL2500039', 'B.Sc Public Administration (ODEL)', '200', 'Male', 'Rivers'])
    writer.writerow([4, 'IYIOLA Kabirat Otindamola', 'ODEL2500123', 'B.Sc Public Administration (ODEL)', '200', 'Female', 'Oyo'])
    writer.writerow([5, 'TIEMO Banro Roland', 'ODEL2500041', 'B.Sc Public Administration (ODEL)', '300', 'Male', 'Delta'])
    return response


@login_required
def export_candidates_csv(request):
    """Exports current admission candidates to CSV."""
    batch_id = request.GET.get('batch')
    candidates = AdmissionCandidate.objects.select_related('batch').all()
    if batch_id:
        candidates = candidates.filter(batch_id=batch_id)
        
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="NSUK_ODeL_Admitted_Students.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['S/N', 'NAME', 'APPLICANT ID', 'PROGRAM', 'LEVEL OF ENTRY', 'SEX', 'STATE', 'BATCH', 'STATUS'])
    
    for idx, c in enumerate(candidates, 1):
        writer.writerow([
            c.serial_number or idx,
            c.candidate_name,
            c.applicant_id,
            c.program,
            c.level_of_entry,
            c.gender,
            c.state_of_origin,
            c.batch.title,
            c.status
        ])
    return response


# --- NEWS & EVENTS MANAGEMENT ---

@login_required
def news_list_dash(request):
    news_qs = NewsEvent.objects.all().order_by('-created_at')
    return render(request, 'dashboard/news/list.html', {'news_list': news_qs})


@login_required
def news_create_dash(request):
    if request.method == 'POST':
        form = NewsEventForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save()
            messages.success(request, f"Article '{news.title}' published successfully!")
            return redirect('dashboard_news')
    else:
        form = NewsEventForm()
    return render(request, 'dashboard/news/form.html', {'form': form, 'title': 'Publish News / Event'})


@login_required
def news_edit_dash(request, pk):
    news = get_object_or_404(NewsEvent, pk=pk)
    if request.method == 'POST':
        form = NewsEventForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, f"Article '{news.title}' updated successfully!")
            return redirect('dashboard_news')
    else:
        form = NewsEventForm(instance=news)
    return render(request, 'dashboard/news/form.html', {'form': form, 'title': f'Edit News: {news.title}', 'news': news})


@login_required
def news_delete_dash(request, pk):
    news = get_object_or_404(NewsEvent, pk=pk)
    if request.method == 'POST':
        title = news.title
        news.delete()
        messages.success(request, f"Article '{title}' deleted.")
        return redirect('dashboard_news')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': f"News / Event: {news.title}",
        'cancel_url': reverse('dashboard_news')
    })


# --- STAFF MANAGEMENT ---

@login_required
def staff_list_dash(request):
    staff_members = StaffMember.objects.all().order_by('sort_order', 'full_name')
    return render(request, 'dashboard/staff/list.html', {'staff_members': staff_members})


@login_required
def staff_create_dash(request):
    if request.method == 'POST':
        form = StaffMemberForm(request.POST, request.FILES)
        if form.is_valid():
            staff = form.save()
            messages.success(request, f"Staff member '{staff.full_name}' added!")
            return redirect('dashboard_staff')
    else:
        form = StaffMemberForm()
    return render(request, 'dashboard/staff/form.html', {'form': form, 'title': 'Add Staff Member'})


@login_required
def staff_edit_dash(request, pk):
    staff = get_object_or_404(StaffMember, pk=pk)
    if request.method == 'POST':
        form = StaffMemberForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, f"Staff member '{staff.full_name}' updated!")
            return redirect('dashboard_staff')
    else:
        form = StaffMemberForm(instance=staff)
    return render(request, 'dashboard/staff/form.html', {'form': form, 'title': f'Edit Staff: {staff.full_name}', 'staff': staff})


@login_required
def staff_delete_dash(request, pk):
    staff = get_object_or_404(StaffMember, pk=pk)
    if request.method == 'POST':
        name = staff.full_name
        staff.delete()
        messages.success(request, f"Staff member '{name}' deleted.")
        return redirect('dashboard_staff')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': f"Staff Member: {staff.full_name} ({staff.position})",
        'cancel_url': reverse('dashboard_staff')
    })


# --- HERO SLIDES MANAGEMENT ---

@login_required
def slide_list_dash(request):
    slides = HeroSlide.objects.all().order_by('display_order', '-created_at')
    return render(request, 'dashboard/slides/list.html', {'slides': slides})


@login_required
def slide_create_dash(request):
    if request.method == 'POST':
        form = HeroSlideForm(request.POST, request.FILES)
        if form.is_valid():
            slide = form.save()
            messages.success(request, f"Hero Slide '{slide.title}' added!")
            return redirect('dashboard_slides')
    else:
        form = HeroSlideForm()
    return render(request, 'dashboard/slides/form.html', {'form': form, 'title': 'Add Hero Slide Banner'})


@login_required
def slide_edit_dash(request, pk):
    slide = get_object_or_404(HeroSlide, pk=pk)
    if request.method == 'POST':
        form = HeroSlideForm(request.POST, request.FILES, instance=slide)
        if form.is_valid():
            form.save()
            messages.success(request, f"Hero Slide '{slide.title}' updated!")
            return redirect('dashboard_slides')
    else:
        form = HeroSlideForm(instance=slide)
    return render(request, 'dashboard/slides/form.html', {'form': form, 'title': f'Edit Slide: {slide.title}', 'slide': slide})


@login_required
def slide_delete_dash(request, pk):
    slide = get_object_or_404(HeroSlide, pk=pk)
    if request.method == 'POST':
        title = slide.title
        slide.delete()
        messages.success(request, f"Hero Slide '{title}' deleted.")
        return redirect('dashboard_slides')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': f"Hero Banner: {slide.title}",
        'cancel_url': reverse('dashboard_slides')
    })


# --- FAQ MANAGEMENT ---

@login_required
def faq_list_dash(request):
    faqs = FAQ.objects.all().order_by('sort_order', 'id')
    return render(request, 'dashboard/faqs/list.html', {'faqs': faqs})


@login_required
def faq_create_dash(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            faq = form.save()
            messages.success(request, f"FAQ '{faq.question}' added!")
            return redirect('dashboard_faqs')
    else:
        form = FAQForm()
    return render(request, 'dashboard/faqs/form.html', {'form': form, 'title': 'Add FAQ'})


@login_required
def faq_edit_dash(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, f"FAQ updated!")
            return redirect('dashboard_faqs')
    else:
        form = FAQForm(instance=faq)
    return render(request, 'dashboard/faqs/form.html', {'form': form, 'title': f'Edit FAQ', 'faq': faq})


@login_required
def faq_delete_dash(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        faq.delete()
        messages.success(request, "FAQ deleted.")
        return redirect('dashboard_faqs')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': f"FAQ: {faq.question}",
        'cancel_url': reverse('dashboard_faqs')
    })


# --- INQUIRIES MANAGEMENT ---

@login_required
def inquiry_list_dash(request):
    status = request.GET.get('status', 'all')
    inquiries_qs = InquiryMessage.objects.all().order_by('-created_at')
    
    if status == 'unread':
        inquiries_qs = inquiries_qs.filter(is_resolved=False)
    elif status == 'resolved':
        inquiries_qs = inquiries_qs.filter(is_resolved=True)
        
    paginator = Paginator(inquiries_qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/inquiries/list.html', {
        'page_obj': page_obj,
        'status_filter': status,
        'total_count': inquiries_qs.count()
    })


@login_required
def inquiry_detail_dash(request, pk):
    inquiry = get_object_or_404(InquiryMessage, pk=pk)
    if request.method == 'POST':
        form = InquiryResponseForm(request.POST, instance=inquiry)
        if form.is_valid():
            form.save()
            messages.success(request, f"Inquiry from {inquiry.full_name} updated.")
            return redirect('dashboard_inquiries')
    else:
        form = InquiryResponseForm(instance=inquiry)
    return render(request, 'dashboard/inquiries/detail.html', {'inquiry': inquiry, 'form': form})


@login_required
def inquiry_delete_dash(request, pk):
    inquiry = get_object_or_404(InquiryMessage, pk=pk)
    if request.method == 'POST':
        name = inquiry.full_name
        inquiry.delete()
        messages.success(request, f"Inquiry from {name} deleted.")
        return redirect('dashboard_inquiries')
    return render(request, 'dashboard/confirm_delete.html', {
        'object_name': f"Inquiry from {inquiry.full_name} ({inquiry.subject})",
        'cancel_url': reverse('dashboard_inquiries')
    })


# --- SITE SETTINGS CONFIGURATION ---

@login_required
def settings_edit_dash(request):
    """Live portal configuration for Director's address, VC note, hotline numbers, portals, etc."""
    setting = SiteSetting.get_settings()
    if request.method == 'POST':
        form = SiteSettingForm(request.POST, request.FILES, instance=setting)
        if form.is_valid():
            form.save()
            messages.success(request, "Site settings and portal configuration updated successfully!")
            return redirect('dashboard_settings')
        else:
            messages.error(request, "Please review the form errors.")
    else:
        form = SiteSettingForm(instance=setting)
    return render(request, 'dashboard/settings/form.html', {'form': form, 'setting': setting})
