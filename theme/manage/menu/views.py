from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.forms import formsets, modelformset_factory
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required, permission_required
from theme.models import Menu, MenuItem, MenuItemContent
from theme.manage.menu.forms import MenuForm, MenuItemForm, MenuItemContentForm, MenuItemReorderForm
from theme.gvars import GENERIC_MODEL_FORM, GENERIC_MODEL_LIST

@login_required
@permission_required('theme.view_menu')
def menu_list(request):
    items = Menu.objects.all()
    new_items = []
    for item in items:
        new_items.append({
            'id': item.id,
            'name': item.name,
            'count': str(item.items.count())
        })
    context = {
        'items': new_items,
        'page_title': _('لیست منو‌های سایت'),
        'fields': ['name', 'count'],
        'headers': [_('نام منو'), _('تعداد آیتم‌های منو')],
        'delete_button_url_name': 'theme_manage_menu_delete',
        'delete_item_title_field': 'name',
        'header_buttons': [
            {
                'title': _('افزودن منوی جدید'),
                'url_name': 'theme_manage_menu_add',
            }
        ],
        'action_buttons': [
            {
                'title': _('ویرایش'),
                'url_name': 'theme_manage_menu_edit',
                'arg1_field': 'id',
            },
            {
                'title': _('آیتم‌های منو'),
                'url_name': 'theme_manage_menuitem_list',
                'arg1_field': 'id'
            }
        ],
        'footer_buttons': [],
    }
    return render(request, GENERIC_MODEL_LIST, context)


@login_required
@permission_required('theme.add_menu')
def menu_add(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('theme_manage_menu_list')
    else:
        form = MenuForm()
    context = {
        'page_title': _('افزودن منوی جدید'),
        'forms': [form],
        'form_submit_url_name': 'theme_manage_menu_add',
        'form_cancel_url_name': 'theme_manage_menu_list',
    }
    return render(request, GENERIC_MODEL_FORM, context)


@login_required
@permission_required('theme.edit_menu')
def menu_edit(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('theme_manage_menu_list')
    else:
        form = MenuForm(instance=menu)
    context = {
        'page_title': _('ویرایش منو'),
        'page_subtitle': menu.name,
        'forms': [form],
        'form_submit_url_name': 'theme_manage_menu_edit',
        'form_submit_url_arg1': menu_id,
        'form_cancel_url_name': 'theme_manage_menu_list',
    }
    return render(request, GENERIC_MODEL_FORM, context)


@login_required
@permission_required('theme.delete_menu')
def menu_delete(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    menu.delete()
    return redirect('theme_manage_menu_list')


@login_required
@permission_required('theme.view_menuitem')
def item_list(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    menu_items = []
    for item in menu.items.all().order_by('parent', 'order'):
        obj = {}
        obj['id'] = item.id
        obj['item_url'] = item.url
        obj['item_parent'] = item.parent.url if item.parent != None else ''
        for lang in settings.LANGUAGES:
            menuitemcontent = item.contents.filter(language=lang[0])
            if menuitemcontent.count() > 0:
                menuitemcontent = menuitemcontent[0]
                obj['item_' + lang[0]
                    ] = menuitemcontent.title if menuitemcontent != None else ''
            else:
                obj['item_' + lang[0]] = ''
        menu_items.append(obj)
    fields = ['item_url', 'item_parent', ]
    headers = [_('آدرس آیتم'), _('والد'),]
    for i in settings.LANGUAGES:
        fields.append('item_' + i[0])
        headers.append(i[0])
    context = {
        'items': menu_items,
        'page_title': _('آیتم‌های منو'),
        'page_subtitle': menu.name,
        'fields': fields,
        'delete_button_url_name': 'theme_manage_menuitem_delete',
        'delete_item_title_field': 'item_url',
        'headers': headers,
        'header_buttons': [
            {
                'title': _('افزودن آیتم جدید'),
                'url_name': 'theme_manage_menuitem_add',
                'url_arg1': menu.id,
            }
        ],
        'action_buttons': [
            {
                'title': _('ویرایش'),
                'url_name': 'theme_manage_menuitem_edit',
                'arg1_field': 'id',
            },
            {
                'title': _('جابجایی'),
                'url_name': 'theme_manage_menuitem_reorder',
                'arg1_field': 'id',
            },
            {
                'title': _('ویرایش محتوای زبان‌ها'),
                'url_name': 'theme_manage_menuitem_contentedit',
                'arg1_field': 'id'
            }
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'theme_manage_menu_list',
            }
        ],
    }
    return render(request, GENERIC_MODEL_LIST, context)


@login_required
@permission_required('theme.add_menuitem')
def item_add(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            menuitem = form.save(commit=False)
            menuitem.menu = menu
            menuitem.save()
            menuitem.order = menuitem.id
            menuitem.save()
            return redirect('theme_manage_menuitem_list', menu_id=menu_id)
    else:
        form = MenuItemForm()
    context = {
        'page_title': _('افزودن آیتم جدید به منو'),
        'page_subtitle': menu.name,
        'forms': [form],
        'form_submit_url_name': 'theme_manage_menuitem_add',
        'form_submit_url_arg1': menu_id,
        'form_cancel_url_name': 'theme_manage_menuitem_list',
        'form_cancel_url_arg1': menu_id,
    }
    return render(request, GENERIC_MODEL_FORM, context)


@login_required
@permission_required('theme.edit_menuitem')
def reorder_item(request, menu_item_id):
    src_item = get_object_or_404(MenuItem, id=menu_item_id)
    if request.method == 'POST':
        form = MenuItemReorderForm(request.POST, menu_item=src_item)
        if form.is_valid():
            dst_item_id = request.POST.get('position')
            dst_item = get_object_or_404(MenuItem, id=dst_item_id)
            order_tmp = src_item.order
            src_item.order = dst_item.order
            dst_item.order = order_tmp
            src_item.save()
            dst_item.save()
            return redirect('theme_manage_menuitem_list', menu_id=src_item.menu.id)
    else:
        form = MenuItemReorderForm(menu_item=src_item)
    context = {
        'page_title': _('ویرایش آیتم منو'),
        'page_subtitle': src_item.url,
        'forms': [form],
        'form_submit_url_name': 'theme_manage_menuitem_reorder',
        'form_submit_url_arg1': menu_item_id,
        'form_cancel_url_name': 'theme_manage_menuitem_list',
        'form_cancel_url_arg1': src_item.menu.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)


@login_required
@permission_required('theme.edit_menuitem')
def item_edit(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('theme_manage_menuitem_list', menu_id=menu_item.menu.id)
    else:
        form = MenuItemForm(instance=menu_item)
    context = {
        'page_title': _('ویرایش آیتم منو'),
        'page_subtitle': menu_item.url,
        'forms': [form],
        'form_submit_url_name': 'theme_manage_menuitem_edit',
        'form_submit_url_arg1': menu_item_id,
        'form_cancel_url_name': 'theme_manage_menuitem_list',
        'form_cancel_url_arg1': menu_item.menu.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)


@login_required
@permission_required('theme.edit_menuitemcontent')
def item_contentedit(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    MenuContentsFormset = modelformset_factory(MenuItemContent, form=MenuItemContentForm, extra=0, max_num=3)
    if request.method == 'POST':
        formset = MenuContentsFormset(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('theme_manage_menuitem_list', menu_id=menu_item.menu.id)
    else:
        for lang in settings.LANGUAGES:
            contents = menu_item.contents.filter(language=lang[0])
            if len(contents) == 0:
                instance = MenuItemContent(title='', language=lang[0], menu_item=menu_item)
                instance.save()
        formset = MenuContentsFormset(queryset=menu_item.contents.all())
    context = {
        'page_title': _('ویرایش محتوای زبان‌ها'),
        'page_subtitle': menu_item.url,
        'formset': formset,
        'form_submit_url_name': 'theme_manage_menuitem_contentedit',
        'form_submit_url_arg1': menu_item_id,
        'form_cancel_url_name': 'theme_manage_menuitem_list',
        'form_cancel_url_arg1': menu_item.menu.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)


@login_required
@permission_required('theme.delete_menuitem')
def item_delete(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    menu_item.delete()
    return redirect('theme_manage_menuitem_list', menu_id=menu_item.menu.id)