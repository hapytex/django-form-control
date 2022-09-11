from django import forms
from form_control.constants import FORM_CONTROL

class FormControlMixin:
    form_control_fields = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # a dict retains the order
            cls = dict.fromkeys(field.widget.attrs.get('class', '').strip().split())
            if FROM_CONTROL not in cls:
                cls[FORM_CONTROL] = None
                field.widget.attrs['class'] = ' '.join(cls)

class FormControlForm(FormControlMixin, forms.Form):
    pass

class FormControlModelForm(FormControlMixin, forms.ModelForm):
    pass
