from .models import SiteSetting, Program, AdmissionBatch, InquiryMessage, NewsEvent

def site_context(request):
    """Context processor providing global settings and quick data to all templates."""
    settings = SiteSetting.get_settings()
    active_programs = Program.objects.filter(is_active=True)[:6]
    latest_batch = AdmissionBatch.objects.filter(is_active=True).first()
    unread_inquiries_count = InquiryMessage.objects.filter(is_resolved=False).count()
    recent_announcements = NewsEvent.objects.filter(is_active=True)[:3]
    
    return {
        'site_settings': settings,
        'global_programs': active_programs,
        'global_latest_batch': latest_batch,
        'unread_inquiries_count': unread_inquiries_count,
        'global_announcements': recent_announcements,
    }
