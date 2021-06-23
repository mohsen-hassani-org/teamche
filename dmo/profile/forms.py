from datetime import datetime
from django import forms
from django.db.models import fields
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from jalali_date import date2jalali
from dmo.models import Dmo, DmoDay, Microaction, Setting
from dmo.profile.utils import jalali_month_length
from team.models import Team

class DmoForm(forms.ModelForm):
    """Form definition for Dmo."""

    class Meta:
        """Meta definition for DmoForm."""

        model = Dmo
        fields = ('goal', 'month', 'year', 'dmo_type', 'color', )

class MicroactionForm(forms.ModelForm):
    """Form definition for Microaction."""

    class Meta:
        """Meta definition for Microactionform."""

        model = Microaction
        fields = ('title',)


def create_days():
    jnow = date2jalali(datetime.now())
    current_month_days = jalali_month_length(jnow)
    days = []
    for d in range(1, current_month_days + 1):
        days.append((d, d))
    return days

class DmoDayForm(forms.ModelForm):
    """Form definition for DmoDay."""
    class Meta:
        """Meta definition for DmoDayform."""
        model = DmoDay
        fields = ('day', 'comment', )
        widgets = {'day': forms.Select(choices=create_days())}


class CloseTeamDmoForm(forms.Form):
    day = forms.IntegerField(label=_('روز'), widget=forms.Select(choices=create_days()))



class TeamEditForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', )
    def __init__(self, *args, **kwargs):
        super(TeamEditForm, self).__init__(*args, **kwargs)
        team = self.instance
        self.fields['dmo_manager'].queryset = team.users.all()


class DmoSettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = ('dmo_manager', )
    def __init__(self, team, *args, **kwargs):
        super(DmoSettingForm, self).__init__(*args, **kwargs)
        self.fields['dmo_manager'].queryset = team.users.all()
