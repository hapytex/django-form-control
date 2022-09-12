from django.contrib.admin import ModelAdmin
from form_control.forms import FormControlModelForm

class FormControlModelAdminMixin:
    form = FormControlModelForm

class FormControlModelAdmin(FormControlModelAdminMixin, ModelAdmin):
    pass
