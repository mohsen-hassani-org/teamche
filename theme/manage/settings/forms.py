from django import forms
from theme.models import SiteSetting
from theme.widgets import ColorWidget

class SiteSettingForm(forms.ModelForm):
    """Form definition for SiteSetting."""
    class Meta:
        """Meta definition for SiteSettingform."""
        model = SiteSetting
        fields = ('__all__')

    # def clean_primary_light_color(self):
    #     primary_light_color = self.cleaned_data.get('primary_light_color')
    #     if primary_light_color and primary_light_color[0] != '#':
    #         primary_light_color = '#' + primary_light_color
    #     return primary_light_color
    # def clean_primary_bold_color(self):
    #     primary_bold_color = self.cleaned_data.get('primary_bold_color')
    #     if primary_bold_color and primary_bold_color[0] != '#':
    #         primary_bold_color = '#' + primary_bold_color
    #     return primary_bold_color
    # def clean_primary_dark_color(self):
    #     primary_dark_color = self.cleaned_data.get('primary_dark_color')
    #     if primary_dark_color and primary_dark_color[0] != '#':
    #         primary_dark_color = '#' + primary_dark_color
    #     return primary_dark_color
    # def clean_accend_light_color(self):
    #     accend_light_color = self.cleaned_data.get('accend_light_color')
    #     if accend_light_color and accend_light_color[0] != '#':
    #         accend_light_color = '#' + accend_light_color
    #     return accend_light_color
    # def clean_accend_bold_color(self):
    #     accend_bold_color = self.cleaned_data.get('accend_bold_color')
    #     if accend_bold_color and accend_bold_color[0] != '#':
    #         accend_bold_color = '#' + accend_bold_color
    #     return accend_bold_color
    # def clean_accend_dark_color(self):
    #     accend_dark_color = self.cleaned_data.get('accend_dark_color')
    #     if accend_dark_color and accend_dark_color[0] != '#':
    #         accend_dark_color = '#' + accend_dark_color
    #     return accend_dark_color