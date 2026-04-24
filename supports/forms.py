from django import forms
from .models import Review, Message, Report

# Add this at the top of every forms.py in all 3 apps
# After saving the form, call this method

def add_bootstrap(form):
    for field in form.fields.values():
        widget = field.widget
        if hasattr(widget, 'attrs'):
            existing = widget.attrs.get('class', '')
            if 'form-control' not in existing and 'form-select' not in existing:
                from django.forms import Select, CheckboxInput
                if isinstance(widget, Select):
                    widget.attrs['class'] = existing + ' form-select'
                elif isinstance(widget, CheckboxInput):
                    widget.attrs['class'] = existing + ' form-check-input'
                else:
                    widget.attrs['class'] = existing + ' form-control'
class ReviewForm(forms.ModelForm):
    class Meta:
        model  = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'rating':  forms.Select(),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model  = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message...'}),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model  = Report
        fields = ['type', 'overview']
        widgets = {
            'overview': forms.Textarea(attrs={'rows': 3}),
        }