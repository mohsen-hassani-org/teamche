from django import forms
from django.utils.translation import ugettext_lazy as _
from theme.models import Theme

class ThemeForm(forms.ModelForm):
    """Form definition for Theme."""

    class Meta:
        """Meta definition for Themeform."""

        model = Theme
        fields = ('name',)


class InstallZipThemeForm(forms.Form):
    zip_file = forms.FileField(label=_('فایل فشرده'))

