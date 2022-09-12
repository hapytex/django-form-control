from django import forms
from django.froms import BaseFormSet, BaseInlineFormSet, formset_factory
from form_control.constants import FORM_CONTROL, CLASS_ATTRIBUTE

class FormControlAttributesMixin:
    form_control = (FORM_CONTROL,)
    form_control_fields = None

    def __init__(self, *args, form_control=None, form_control_fields=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_form_control_attrs(form_control, form_control_fields)

    def _set_form_control_attrs(form_control=None, form_control_fields=None):
        if form_control is not None:
            if isinstance(form_control, str):
                form_control = (form_control,)
            self.form_control = form_control
        if form_control_fields is not None:
            self.form_control_fields = form_control_fields

    def _add_form_control_to_fields(self, form, fields, form_control_attr):
        if self.form_control_fields is None:
            fields = form.fields.values()
        else:
            fields = map(form.fields.get, self.form_control_fields)
        form_control_attr = dict.fromkeys(self.form_control)
        for field in fields:
            if field is not None:
                self._add_form_control_to_widget(field.widget, form_control_attr)

    def _add_form_control_to_widget(self, widget, form_control_attr):
            attrs = widget.attrs
            # a dict retains the order
            cls = dict.fromkeys(attrs.get(CLASS_ATTRIBUTE, '').split())
            cls.update(form_control_attr)
            attrs[CLASS_ATTRIBUTE] = ' '.join(cls)


class FormControlMixin(FormControlAttributesMixin):
    def __init__(self, *args, form_control=None, form_control_fields=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_form_control_to_fields(self)


class FormControlSetMixin(FormControlAttributesMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            if not isinstance(form, FormControlMixin):
                self._add_form_control_to_fields(form)
        self._add_form_control_to_fields(self.management_form)


class FormControlForm(FormControlMixin, forms.Form):
    pass


class FormControlModelForm(FormControlMixin, forms.ModelForm):
    pass


class BaseFormControlFormSet(FormControlSetMixin, BaseFormSet):
    pass


class BaseFormControlInlineFormSet(FormControlSetMixin, BaseInlineFormSet):
    pass

def formcontrol_formset_factory(*args, **kwargs):
    if len(args) < 2:
        kwargs.setdefault('formset', BaseFormControlFormSet)
    return formset_factory(*args, **kwargs)
