from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from jalali_date import date2jalali
from dmo.profile.utils import jalali_month_length
from dmo.model_fields import ColorField

# Create your models here.
class Dmo(models.Model):
    class Meta:
        verbose_name = 'DMO'
        verbose_name_plural = 'DMOs'

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
    dmo_type = models.CharField(max_length=10, choices=[('public', _('عمومی')), ('private', _('خصوصی'))], verbose_name=_('نوع DMO'), default='private')
    color = ColorField(default='#4287f5', verbose_name=_('رنگ'))
    month = models.PositiveSmallIntegerField(verbose_name=_('ماه'), default=current_month, validators=[
                                             MinValueValidator(1), MaxValueValidator(12)])
    year = models.PositiveSmallIntegerField(default=current_year, verbose_name=_('سال'), validators=[
                                            MinValueValidator(1390), MaxValueValidator(1499)])

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
