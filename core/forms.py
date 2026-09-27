from django import forms
from .models import InquiryMessage

class ContactInquiryForm(forms.ModelForm):
    class Meta:
        model = InquiryMessage
        fields = ['full_name', 'email', 'phone', 'program_of_interest', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all outline-none',
                'placeholder': 'Your Full Name (e.g. Ibrahim Adamu)',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all outline-none',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all outline-none',
                'placeholder': '+234 800 000 0000',
            }),
            'program_of_interest': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all outline-none',
                'placeholder': 'e.g. B.Sc Public Administration',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all outline-none',
                'placeholder': 'Subject / Topic of your inquiry',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all outline-none',
                'placeholder': 'How can we help you today? Please provide any details about your academic background or inquiries...',
                'rows': 5,
                'required': True
            }),
        }
