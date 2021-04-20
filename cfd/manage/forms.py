from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from cfd.models import Asset
from cfd.manage import views

class AssetForm(forms.ModelForm):
    """Form definition for Asset."""
    class Meta:
        """Meta definition for Assetform."""
        model =Asset
        fields = ('name',)
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if '/' not in name:
            raise ValidationError(_('دارایی باید حتما شامل کاراکتر / باشد'))
        pairs = name.split('/')
        if len(pairs) > 2:
            raise ValidationError('دارایی نباید شامل بیش از دو کاراتر / باشد')
        new_asset = '{}/{}'.format(pairs[0].upper(), pairs[1].upper())
        return new_asset
        
