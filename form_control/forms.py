from django import forms
from form_control.constants import FORM_CONTROL

class FormControlMixin:
    form_control_fields = None
    form_control = FORM_CONTROL
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.form_control_fields is None:
            fields = self.fields.values()
        else:
            fields = map(self.fields.get, self.form_control_fields)
        form_control_attr = self.form_control
        for field in fields:
            if field is not None:
                attrs = field.widget.attrs
                # a dict retains the order
                cls = dict.fromkeys(attrs.get('class', '').strip().split())
                if form_control_attr not in cls:
                    cls[form_control_attr] = None
                    attrs['class'] = ' '.join(cls)


class FormControlForm(FormControlMixin, forms.Form):
    pass


class FormControlModelForm(FormControlMixin, forms.ModelForm):
    pass
