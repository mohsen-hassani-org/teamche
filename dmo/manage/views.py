from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import ugettext as _
from dmo.models import Dmo, DmoDay, Microaction
from dmo.gvars import ALL_PUBLIC_DMO,DMO_CHART_TEMPLATE,DMO_IMAGE_TEMPLATE,DMO_TABLE_TEMPLATE
from dmo.gvars import GENERIC_MODEL_FORM, GENERIC_MODEL_LIST


@login_required
@permission_required('dmo.view_dmo')
def view_dmos(request):
    dmos = Dmo.objects.all()
    data = {
        'items': dmos,
        'fields': ['user', 'goal', 'dmo_type', 'year', 'month', ],
        'headers': [_('کاربر'), _('هدف'), _('نوع'), _('سال'), _('ماه')],
        'page_title': _('همه DMOها'),
        'action_buttons': [
            {
                'title': _('ریزعملکرد'),
                'url_name': 'dmo_manage_dmoday_view',
                'arg1_field': 'id',
            },
            {
                'title': _('مشاهده حالت جدولی'),
                'url_name': 'dmo_profile_dmo_view_table',
                'arg1_field': 'id',
                'new_tab': True,
            },
        ],
    }
    return render(request, GENERIC_MODEL_LIST, data)

@login_required
@permission_required('dmo.view_dmoday')
def view_dmoday(request, dmo_id):
    dmo = get_object_or_404(Dmo, id=dmo_id)
    dmodays = dmo.days.all()
    items = []
    for dmoday in dmodays:
        items.append({
            'id': dmoday.id,
            'day': _('روز {day}'.format(day=dmoday.day)),
            'done': _('انجام شده') if dmoday.done else _('انجام نشده'),
            'comment': dmoday.comment,
        })
    context = {
        'page_title': _('ریز عملکرد DMO'),
        'page_subtitle': dmo,
        'items': items,
        'fields': ['day', 'done', 'comment', ],
        'headers': [_('روز'), _('وضعیت'), _('توضیحات'), ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'dmo_manage_dmo_view_all',
            }
        ],
        'delete_button_url_name': 'dmo_manage_dmoday_delete',
    }
    return render(request, GENERIC_MODEL_LIST, context)


@login_required
@permission_required('dmo.dmoday_delete')
def dmoday_delete(request, dmoday_id):
    dmoday = get_object_or_404(DmoDay, id=dmoday_id)
    dmoday.delete()
    return redirect('dmo_manage_dmoday_view', dmo_id=dmoday.dmo.id)

