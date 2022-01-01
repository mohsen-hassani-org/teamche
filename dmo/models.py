from datetime import datetime
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from jalali_date import date2jalali
from dmo.profile.utils import jalali_month_length
from dmo.model_fields import ColorField
from team.models import Team

# Create your models here.


class DmoManager(models.Manager):
    def get_team_month_dmo(self, user, team):
        jnow = date2jalali(datetime.now())
        dmos = Dmo.objects.filter(Q(month=jnow.month), Q(year=jnow.year),
                Q(Q(dmo_type=Dmo.DmoTypes.TEAM) | Q(dmo_type=Dmo.DmoTypes.PUBLIC)), Q(team=team), ~Q(user=user)).order_by('user')
        return dmos

    def get_my_team_month_dmo(self, user, team):
        jnow = date2jalali(datetime.now())
        dmos = Dmo.objects.filter(month=jnow.month, year=jnow.year, user=user, team=team)
        return dmos


class Dmo(models.Model):
    class Meta:
        verbose_name = 'DMO'
        verbose_name_plural = 'DMOs'

    class DmoTypes(models.TextChoices):
        PUBLIC = 'public', _('عمومی')
        PRIVATE = 'private', _('خصوصی')
        TEAM = 'team', _('تیمی')

    def __str__(self):
        return '{user}: {year}/{month} - {goal}'.format(user=self.user, month=self.month, year=self.year, goal=self.goal)

    def current_month():
        jnow = date2jalali(datetime.now())
        return jnow.month

    def current_year():
        jnow = date2jalali(datetime.now())
        return jnow.year

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='dmo_set', verbose_name=_('کاربر'))
    goal = models.CharField(max_length=200, verbose_name=_('هدف'))
    dmo_type = models.CharField(max_length=10, choices=DmoTypes.choices, verbose_name=_(
        'نوع DMO'), default=DmoTypes.PRIVATE)
    color = ColorField(default='#4287f5', verbose_name=_('رنگ'))
    month = models.PositiveSmallIntegerField(verbose_name=_('ماه'), default=current_month, validators=[
                                             MinValueValidator(1), MaxValueValidator(12)])
    year = models.PositiveSmallIntegerField(default=current_year, verbose_name=_('سال'), validators=[
                                            MinValueValidator(1390), MaxValueValidator(1499)])
    team = models.ForeignKey(Team, on_delete=models.SET_NULL,
                             null=True, verbose_name=_('تیم'), related_name='dmos')
    contents = DmoManager()
    objects = models.Manager()

    def days_to_data(self):
        dmo_days = self.days.all().order_by('day')
        procedure = 0
        step = 0
        data = {}
        for dmo_day in dmo_days:
            procedure = procedure + 1 if dmo_day.done else procedure - 1
            step += 1
            if  step == 1 and procedure == -1:
                procedure = 0
            data[dmo_day.day] = procedure
        return data

    def get_summary_as_table(self):
        dmo_data = self.days_to_data()
        jnow = date2jalali(datetime.now())
        today = jnow.day
        if today < 10:
            today = 10
        classes = []
        tmp = 0
        table = '<table class="dmo_summary"><tr>'
        for i in range(1, today + 1):
            if i in dmo_data.keys():
                if dmo_data[i] > tmp:
                    classes.append({'day': i, 'color': 'green'})
                else:
                    classes.append({'day': i, 'color': 'red'})
                tmp = dmo_data[i]
            else:
                classes.append({'day': i, 'color': 'gray'})
        classes = classes[-10:]
        for klass in classes:
            table += '<td class="{color}">{day}</td>'.format(color=klass['color'], day=klass['day'])
        table += '</tr></table>'
        return table

class Setting(models.Model):
    class Meta:
        verbose_name = _('تنظیم DMO')
        verbose_name_plural = _('تنظیمات DMO')
    team = models.OneToOneField(Team, verbose_name=_('تیم'), on_delete=models.CASCADE, related_name='dmo_settings')
    dmo_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('مدیر DMO'))
    discord_webhook = models.URLField(verbose_name=_('Webhook دیسکورد'), blank=True)

class Microaction(models.Model):
    class Meta:
        verbose_name = _('میکرواکشن')
        verbose_name_plural = _('میکرواکشن‌ها')

    def __str__(self):
        return '{dmo} --> {title}'.format(dmo=self.dmo, title=self.title)
    dmo = models.ForeignKey(Dmo, on_delete=models.CASCADE,
                            related_name='microactions', verbose_name='Dmo')
    title = models.CharField(max_length=200, verbose_name=_('عنوان'))


class DmoDay(models.Model):
    class Meta:
        verbose_name = _('روز Dmo')
        verbose_name_plural = _('روزهای Dmo')

    def __str__(self):
        return '{day}: {stat}'.format(day=self.day, stat=self.done)

    def current_day():
        jnow = date2jalali(datetime.now())
        return jnow.day

    def current_month_days():
        jnow = date2jalali(datetime.now())
        return jalali_month_length(jnow)

    dmo = models.ForeignKey(Dmo, on_delete=models.CASCADE,
                            related_name='days', verbose_name='Dmo')
    day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(
        current_month_days)], default=current_day, verbose_name=_('روز'))
    done = models.BooleanField(verbose_name=_('انجام شده'))
    comment = models.CharField(
        max_length=200, null=True, blank=True, verbose_name=_('توضیحات'))
    user_locked = models.BooleanField(verbose_name=_('قفل کاربر'), default=False)
