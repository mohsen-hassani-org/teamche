from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from datetimewidget.widgets import DateTimeWidget
from django_summernote.widgets import SummernoteWidget
from team.models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.DateInput):
    input_type = 'time'

class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', )

class TeamInvitationForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.none(), label=_('کاربران'))
    def __init__(self, user, *args, **kwargs):
        super(TeamInvitationForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.exclude(id=user.id)

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ('title', 'datetime', )
        widgets = {
            'datetime': DateTimeWidget(bootstrap_version=3, usel10n=True),
        }

class ProceddingsForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ('proceedings',)

class AttendanceForm(forms.ModelForm):
    """Form definition for Attendance."""
    class Meta:
        """Meta definition for Attendanceform."""
        model = Attendance
        fields = ('user', 'attendance_type', 'leave_hours', )
        widgets = {
            'attendance_type': forms.widgets.RadioSelect(),
        }
    def __init__(self, team, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self._team = team
        self.fields['user'].queryset = team.users.all() 
    def clean_user(self):
        user = self.cleaned_data['user']
        if user not in self._team.users.all():
            raise ValidationError(_('این کاربر در این تیم عضو نیست'))
        return user

        
class AttendanceFormWithDate(forms.ModelForm):
    """Form definition for Attendance."""
    class Meta:
        """Meta definition for Attendanceform."""
        model = Attendance
        fields = ('user', 'date', 'attendance_type', 'leave_hours', )
        widgets = {
            'attendance_type': forms.widgets.RadioSelect(),
        }
    def __init__(self, team, *args, **kwargs):
        super(AttendanceFormWithDate, self).__init__(*args, **kwargs)
        self._team = team
        self.fields['user'].queryset = team.users.all() 
    def clean_user(self):
        user = self.cleaned_data['user']
        if user not in self._team.users.all():
            raise ValidationError(_('این کاربر در این تیم عضو نیست'))
        return user


        
class AttendanceSearchForm(forms.Form):
    TYPES = [(None, '----------')]
    TYPES += Attendance.AttendanceType.choices
    user = forms.ModelChoiceField(queryset=User.objects.none(), required=False, label='کاربر')
    att_type = forms.ChoiceField(choices=TYPES, required=False, label='نوع حضوری')
    sdate = forms.DateField(required=False, widget=DateInput(), label='از تاریخ')
    edate = forms.DateField(required=False, widget=DateInput(), label='تا تاریخ')
    def __init__(self, team, *args, **kwargs):
        super(AttendanceSearchForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = team.users.all()
    


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('title', 'due_datetime', 'vote_type', )
        widgets = {
            'due_datetime': DateTimeInput(),
        }

class VoteChoiceForm(forms.ModelForm):
    class Meta:
        model = VoteChoice
        fields = ('choice', )