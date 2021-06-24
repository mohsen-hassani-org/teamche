from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django_quill.fields import QuillField
from accounts.models import AccountSetting


# Create your models here.

def file_size_validator(avatar):
    vs = avatar.size
    setting = AccountSetting.objects.last()
    max_size = 2
    if setting is not None:
        max_size = setting.avatar_max_file_size
    max_size_b = max_size * 1024 * 1024
    if vs > max_size_b:
        raise ValidationError(
            _('سایز فایل شما بیشتر از حد مجاز است. حداکثر حجم مجاز فایل {0} مگابایت می‌باشد.'.format(max_size)))
    else:
        return avatar


class Team(models.Model):
    class Meta:
        verbose_name = _('تیم')
        verbose_name_plural = _('تیم‌ها')
        permissions = (
            ('manage_team', _('مدیریت تیم')),
        )
    def __str__(self):
        return self.name
    name = models.CharField(max_length=50, verbose_name=_('نام تیم'))
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='teams_as_leader', verbose_name=_('رهبر'))
    users = models.ManyToManyField(User, related_name='teams', verbose_name=('اعضا'))
    avatar = models.ImageField(max_length=300, upload_to='team/avatars', default='team/avatar.png',
                               validators=[file_size_validator], verbose_name=_('تصویر نمایه'), null=True, blank=True)

class TeamInvitation(models.Model):
    class Meta:
        verbose_name = _('دعوتنامه تیم')
        verbose_name_plural = _('دعوتنامه‌های تیم')
    class ActionTypes(models.TextChoices):
        ACCEPT = 'ac', _('پذیرفتن')
        REJECT = 'rj', _('رد کردن')
        NO_ACTION = 'n', _('بدون عمل')
    def __str__(self):
        return '{team}: {user}_{date}'.format(team=self.team, user=self.user, date=self.request_datetime)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invitations', verbose_name=_('تیم'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_invitations', verbose_name=_('کاربر'))
    request_datetime = models.DateTimeField(auto_created=True)
    action = models.CharField(max_length=2, choices=ActionTypes.choices, default=ActionTypes.NO_ACTION)
    action_datetime = models.DateTimeField(null=True, verbose_name=_('تاریخ عملیات'))

class Meeting(models.Model):
    class Meta:
        verbose_name = _('جلسه')
        verbose_name_plural = _('جلسات')
    def __str__(self):
        return '{title} - {date}'.format(title=self.title, date=self.datetime)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='meetings', verbose_name=_('تیم'))
    datetime = models.DateTimeField(verbose_name=_('تاریخ جلسه'), default=datetime.now)
    title = models.CharField(max_length=100, verbose_name=_('عنوان جلسه'))
    proceedings = QuillField(null=True, blank=True, verbose_name=_('صورتجلسه'))
    

class MeetingSigature(models.Model):
    class Meta:
        verbose_name = _('امضا جلسه')
        verbose_name_plural = _('امضا جلسات')
        unique_together = ('meeting', 'user', )
    def __str__(self):
        return '{meeting} - {user}'.format(meeting=self.meeting, user=self.user)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='signatures', verbose_name=_('جلسه'))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='signatures', verbose_name=_('کاربر'))
    sign_date = models.DateTimeField(null=True, blank=True, verbose_name=_('تاریخ امضا'))


class Attendance(models.Model):
    class Meta:
        verbose_name = _('حضور و غیاب')
        verbose_name_plural = _('حضور و غیاب‌ها')
        unique_together = ('user', 'date', )
    class AttendanceType(models.TextChoices):
        PRESENT = 'p', _('حاضر')
        ABSENT = 'a', _('عدم حضور')
        LEAVE = 'l', _('مرخصی کامل')
        MINUTE_LEAVE = 'h', _('مرخصی (دقیقه)')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='attendances', verbose_name=_('تیم'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances', verbose_name=_('کاربر'))
    date = models.DateField(verbose_name=_('تاریخ'), default=datetime.now)
    attendance_type = models.CharField(max_length=1, choices=AttendanceType.choices, verbose_name=_('نوع حضور'), default=AttendanceType.ABSENT)
    leave_minutes = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('مدت مرخصی (دقیقه)'))



class Vote(models.Model):
    class Meta:
        verbose_name = _('نظرسنجی')
        verbose_name_plural = _('نظرسنجی‌ها')
    class VoteTypes(models.TextChoices):
        PUBLIC = 'pub', _('عمومی')
        SECRET = 'sec', _('مخفی')
    def __str__(self):
        return self.title
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='votes', verbose_name=_('تیم'))
    title = models.CharField(max_length=200, verbose_name=_('عنوان نظرسنجی'))
    publish_datetime = models.DateTimeField(auto_now=True)
    due_datetime = models.DateTimeField(verbose_name=_('مهلت'))
    vote_type = models.CharField(max_length=3, choices=VoteTypes.choices, default=VoteTypes.PUBLIC, verbose_name=_('نوع نظرسنجی'))

class VoteChoice(models.Model):
    class Meta:
        verbose_name = _('گزینه')
        verbose_name_plural = _('گزینه‌ها')
    def __str__(self):
        return self.choice
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='choices', verbose_name=_('نظرسنجی'))
    choice =  models.CharField(max_length=200, verbose_name=_('گزینه'))

class UserVote(models.Model):
    class Meta:
        verbose_name = _('نظر کاربر')
        verbose_name_plural = _('نظرات کاربران')
        unique_together = ('user', 'user_choice', )
    def __str__(self):
        return '{user}: {vote}'.format(user=self.user, vote=self.user_choice)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes', verbose_name=_('کاربر'))
    user_choice = models.ForeignKey(VoteChoice, on_delete=models.CASCADE, related_name='user_votes', verbose_name=_('انتخاب کاربر'))
    voted_date = models.DateTimeField(auto_created=True)