from django.template.defaulttags import register
from dmo.profile.utils import month_num_to_str

@register.filter
def month_name(month):
    return month_num_to_str(month)
