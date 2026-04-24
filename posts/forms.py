from django import forms
from .models import TuitionPost, TuitionApplication, Payment


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

class TuitionPostForm(forms.ModelForm):
    class Meta:
        model  = TuitionPost
        fields = ['s_class', 'mode', 'date', 'gender', 'time_slot',
                  'address', 'salary', 'subject', 'version', 'description']
        widgets = {
            'date':        forms.DateInput(attrs={'type': 'date'}),
            'address':     forms.Textarea(attrs={'rows': 2}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class TuitionApplicationForm(forms.ModelForm):
    class Meta:
        model  = TuitionApplication
        fields = []   # teacher & post set in view


class PaymentForm(forms.ModelForm):
    class Meta:
        model  = Payment
        fields = ['amount', 'method']