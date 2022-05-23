from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext as _


User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('نام'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_(
        'کاربر'), related_name='tags')
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey(content_type, object_id)
    

    class Meta:
        verbose_name = _('برچسب')
        verbose_name_plural = _('برچسب')
