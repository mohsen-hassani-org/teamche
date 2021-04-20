from django import forms
from django.utils.translation import ugettext as _
from theme.models import PageCategory, PageImage, PageLink, PageMenu, PagePost, PageText
from theme.models import PageTextContent, PageImageContent, PageLinkContent, PageCategoryContent, PageMenuContent

class PageTextContentSingleLanguageForm(forms.ModelForm):
    class Meta:
        model = PageTextContent
        fields = ('text_value', 'language')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].disabled = True
    
class PageTextContentNoLanguageForm(forms.ModelForm):
    class Meta:
        model = PageTextContent
        fields = ('text_value',)
        help_texts = {
            'text_value': _('توجه: این مقدار برای تمامی زبان‌ها اعمال خواهد شد و تمامی محتواهای قبلی این متغیر پاک خواهند شد.')
        }


class PageImageContentSingleLanguageForm(forms.ModelForm):
    class Meta:
        model = PageImageContent
        fields = ('image_value', 'language')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].disabled = True
  
class PageImageContentNoLanguageForm(forms.ModelForm):
    class Meta:
        model = PageImageContent
        fields = ('image_value',)
        help_texts = {
            'image_value': _('توجه: این مقدار برای تمامی زبان‌ها اعمال خواهد شد و تمامی محتواهای قبلی این متغیر پاک خواهند شد.')
        }



class PageLinkContentSingleLanguageForm(forms.ModelForm):
    class Meta:
        model = PageLinkContent
        fields = ('link_value', 'language')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].disabled = True

class PageLinkContentNoLanguageForm(forms.ModelForm):
    class Meta:
        model = PageLinkContent
        fields = ('link_value',)
        help_texts = {
            'link_value': _('توجه: این مقدار برای تمامی زبان‌ها اعمال خواهد شد و تمامی محتواهای قبلی این متغیر پاک خواهند شد.')
        }


class PageMenuContentSingleLanguageForm(forms.ModelForm):
    class Meta:
        model = PageMenuContent
        fields = ('menu_content', 'language')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].disabled = True

class PageMenuContentNoLanguageForm(forms.ModelForm):
    class Meta:
        model = PageMenuContent
        fields = ('menu_content',)
        help_texts = {
            'link_value': _('توجه: این مقدار برای تمامی زبان‌ها اعمال خواهد شد و تمامی محتواهای قبلی این متغیر پاک خواهند شد.')
        }



class PageCatContentSingleLanguageForm(forms.ModelForm):
    class Meta:
        model = PageCategoryContent
        fields = ('category_content', 'language')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].disabled = True

class PageCatContentNoLanguageForm(forms.ModelForm):
    class Meta:
        model = PageCategoryContent
        fields = ('category_content',)
        help_texts = {
            'link_value': _('توجه: این مقدار برای تمامی زبان‌ها اعمال خواهد شد و تمامی محتواهای قبلی این متغیر پاک خواهند شد.')
        }

