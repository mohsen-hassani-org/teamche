from django.db import models
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from accounts import strings
from accounts import gvars

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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=11, null=True, blank=True, verbose_name=_('شماره تماس'))
    avatar = models.ImageField(max_length=300, upload_to='account/avatars', default='account/profile.png',
                               validators=[file_size_validator], verbose_name=_('تصویر نمایه'))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_('تاریخ تولد'))

    class Meta:
        def __str__(self):
            return self.user.username
        verbose_name = strings.MODEL_PROFILE
        verbose_name_plural = strings.MODEL_PROFILES
        permissions = [
            ('edit_permission', strings.MODPERM_EDIT_PERM),
            ('view_user', strings.MODPERM_VIEW_USER),
            ('add_user', strings.MODPERM_ADD_USER),
            ('edit_user', strings.MODPERM_EDIT_USER),
            ('edit_user_pass', strings.MODPERM_EDIT_USER_PASS),
            ('delete_user', strings.MODPERM_DEL_USER),
            ('view_group', strings.MODPERM_VIEW_GROUP),
            ('add_group', strings.MODPERM_ADD_GROUP),
            ('edit_group', strings.MODPERM_EDIT_GROUP),
            ('group_membership', strings.MODPERM_GROUP_MEMBER),
            ('delete_group', strings.MODPERM_DEL_GROUP),
        ]

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        uname = self.user.username
        fname = self.user.first_name
        lname = self.user.last_name
        return '{code} ({fn} {ln})'.format(code=uname, fn=fname, ln=lname)

    @property
    def display_name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        first_name = self.user.first_name
        last_name = self.user.last_name
        return f"https://ui-avatars.com/api/?name={first_name}+{last_name}"

def user_str_function(self):
    return '{fn} {ln} ({un})'.format(fn=self.first_name, ln=self.last_name, un=self.username)

class AccountSetting(models.Model):
    class Meta:
        verbose_name_plural = strings.MODEL_ACCOUNT_SETTING
        verbose_name = strings.MODEL_ACCOUNT_SETTING
        permissions = [
            ('edit_setting', _('ویرایش تنظیمات')),
        ]
    user_can_register = models.BooleanField(
        default=True, verbose_name=_('اجازه ثبت‌نام در سایت'))
    # only_admin_can_login = models.BooleanField(
    # default=False, verbose_name=_('اجازه ورود کاربران غیر مدیر'))
    avatar_max_file_size = models.PositiveSmallIntegerField(default=2, verbose_name=_(
        'حجم مجاز آپلود تصویر نمایه (مگابایت)'), validators=[MinValueValidator(1), MaxValueValidator(50)])

User.add_to_class('__str__', user_str_function)