from django import forms
from django.utils.translation import ugettext as _
from theme.models import Page, ThemePage

class CustomPageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('slug', 'theme_page', 'base', 'post', )
    def __init__(self, *args, **kwargs):
        super(CustomPageForm, self).__init__(*args, **kwargs)
        self.fields['theme_page'].queryset = ThemePage.objects.filter(theme__is_active=True).filter(page_type='post')
        self.fields['base'].queryset = Page.objects.filter(theme_page__theme__is_active=True).filter(theme_page__page_type='base')
    
